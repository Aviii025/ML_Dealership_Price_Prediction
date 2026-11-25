"""Purchase-price estimation for second-hand vehicles.

Cars use ``models/car_model.pkl``; scooters and bikes share
``models/two_wheeler_model.pkl``. Both are bundles written by
``training/train.py``. The model predicts the market value for a vehicle in
typical condition, and condition, insurance, accident and document
adjustments are applied on top. Without a model file, or for fuel types the
model never saw (e.g. electric), a transparent rule-based estimate is used.
"""

from __future__ import annotations

import pickle
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import pandas as pd

from src import features
from src.config import TYPICAL_KM_PER_YEAR, current_year

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"

# First-year drop followed by a yearly depreciation rate, per vehicle type.
FIRST_YEAR_DROP = {"car": 0.15, "scooter": 0.18, "bike": 0.15}
YEARLY_DEPRECIATION = {"car": 0.10, "scooter": 0.12, "bike": 0.10}
MIN_RESIDUAL = 0.10

CONDITION_FACTOR = {"Excellent": 1.05, "Good": 1.00, "Fair": 0.90, "Poor": 0.75}
OWNER_FACTOR = {"1st Owner": 1.00, "2nd Owner": 0.93, "3rd Owner": 0.87, "4th Owner or more": 0.80}
INSURANCE_FACTOR = {"Comprehensive": 1.02, "Third Party": 1.00, "Expired / None": 0.97}
ACCIDENT_FACTOR = 0.85
MISSING_DOCS_FACTOR = 0.90
DEALER_MARGIN = 0.12


@dataclass
class Valuation:
    """Result of a valuation: market value plus the dealer's offer range."""

    market_value: float
    offer_low: float
    offer_high: float
    source: str
    notes: list[str] = field(default_factory=list)


def age_factor(vehicle_type: str, year: int) -> float:
    """Share of the original price retained after depreciation by age."""
    age = max(current_year() - year, 0)
    if age == 0:
        return 1.0
    retained = (1 - FIRST_YEAR_DROP[vehicle_type]) * (1 - YEARLY_DEPRECIATION[vehicle_type]) ** (age - 1)
    return max(retained, MIN_RESIDUAL)


def mileage_factor(vehicle_type: str, year: int, km_driven: int) -> float:
    """Penalty/bonus for mileage relative to typical usage for the age."""
    age = max(current_year() - year, 1)
    expected = TYPICAL_KM_PER_YEAR[vehicle_type] * age
    ratio = km_driven / expected if expected else 1.0
    if ratio <= 0.5:
        return 1.05
    if ratio <= 1.0:
        return 1.0
    if ratio <= 1.5:
        return 0.93
    return 0.85


def apply_condition_adjustments(value: float, details: dict, notes: list[str]) -> float:
    """Factors the training data doesn't capture: condition, insurance, accidents, documents."""
    value *= CONDITION_FACTOR.get(details.get("condition", "Good"), 1.0)
    value *= INSURANCE_FACTOR.get(details.get("insurance", "Third Party"), 1.0)
    if details.get("accident_history"):
        value *= ACCIDENT_FACTOR
        notes.append("Accident history reduces the offer.")
    if not details.get("documents_complete", True):
        value *= MISSING_DOCS_FACTOR
        notes.append("Incomplete documents (RC / service records) reduce the offer.")
    return value


def rule_based_value(vehicle_type: str, details: dict) -> Valuation:
    """Estimate market value from the original price using simple factors."""
    notes: list[str] = []
    value = float(details["original_price"])
    value *= age_factor(vehicle_type, details["year"])

    m = mileage_factor(vehicle_type, details["year"], details["km_driven"])
    if m < 1:
        notes.append("Mileage is higher than typical for its age.")
    value *= m
    value *= OWNER_FACTOR.get(details.get("owners", "1st Owner"), 1.0)
    value = apply_condition_adjustments(value, details, notes)
    return _with_offer_range(value, "rule-based estimate", notes)


# Which saved model serves each vehicle type, and how to build its features.
MODEL_FILES = {"car": "car", "scooter": "two_wheeler", "bike": "two_wheeler"}


@lru_cache(maxsize=None)
def _load_model(name: str):
    path = MODELS_DIR / f"{name}_model.pkl"
    if not path.exists():
        return None
    with path.open("rb") as fh:
        return pickle.load(fh)


def _with_offer_range(market_value: float, source: str, notes: list[str]) -> Valuation:
    offer_mid = market_value * (1 - DEALER_MARGIN)
    return Valuation(
        market_value=round(market_value, -2),
        offer_low=round(offer_mid * 0.95, -2),
        offer_high=round(offer_mid * 1.05, -2),
        source=source,
        notes=notes,
    )


def ml_value(vehicle_type: str, details: dict, bundle: dict) -> Valuation:
    """Market value from a trained model bundle (see ``training/train.py``)."""
    record = pd.DataFrame([{**details, "segment": vehicle_type}])
    make = features.car_features if bundle["feature_set"] == "car" else features.two_wheeler_features
    value = float(bundle["pipeline"].predict(make(record))[0])
    notes: list[str] = []
    value = apply_condition_adjustments(value, details, notes)
    year = bundle.get("data_reference_year")
    return _with_offer_range(value, f"ML model (trained on {year} listings)" if year else "ML model", notes)


def estimate_price(vehicle_type: str, details: dict) -> Valuation:
    """Return a valuation, preferring a trained model when one is available."""
    if vehicle_type not in FIRST_YEAR_DROP:
        raise ValueError(f"Unknown vehicle type: {vehicle_type!r}")

    bundle = _load_model(MODEL_FILES[vehicle_type])
    if bundle is None:
        return rule_based_value(vehicle_type, details)

    fuel = details.get("fuel_type")
    if fuel and fuel not in bundle.get("supported_fuels", [fuel]):
        fallback = rule_based_value(vehicle_type, details)
        fallback.notes.insert(0, f"The ML model has no {fuel} vehicles in its training data, "
                                 "so a rule-based estimate was used.")
        return fallback

    try:
        return ml_value(vehicle_type, details, bundle)
    except Exception as exc:  # fall back rather than break the form
        fallback = rule_based_value(vehicle_type, details)
        fallback.notes.insert(0, f"ML model failed ({exc}); used rule-based estimate.")
        return fallback
