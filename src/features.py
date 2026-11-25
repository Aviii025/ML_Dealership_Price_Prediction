"""Turn form inputs into model features.

Used by both the training script and the app, so a record is transformed the
same way at training and prediction time. Records use the app's field names
(``brand``, ``model``, ``year``, ``km_driven``, ``owners``, ...).
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd

from src.config import current_year

# Words that belong to the brand and should not be taken as the model name.
_BRAND_WORDS = {
    "maruti", "suzuki", "royal", "enfield", "harley", "davidson", "mercedes",
    "benz", "land", "rover", "ola", "electric", "hero", "honda", "bajaj", "tvs",
    "yamaha", "ktm", "kawasaki", "triumph", "jawa", "ather", "vespa", "aprilia",
    "hyundai", "tata", "mahindra", "toyota", "kia", "renault", "volkswagen",
    "skoda", "mg", "ford", "nissan", "chevrolet", "datsun", "fiat", "jeep",
    "bmw", "audi", "volvo", "jaguar", "lexus", "motocorp",
}

OWNER_RANK = {"1st Owner": 1, "2nd Owner": 2, "3rd Owner": 3, "4th Owner or more": 4}

CAR_CATEGORICAL = ["brand", "model_name", "fuel_type", "transmission", "seller_type"]
CAR_NUMERIC = ["age", "km_driven", "owner_rank", "engine_cc", "seats"]

TWO_WHEELER_CATEGORICAL = ["segment", "brand", "model_name", "seller_type"]
TWO_WHEELER_NUMERIC = ["age", "km_driven", "owner_rank", "log_original_price"]


def model_name(brand: str, model_text: str) -> str:
    """First meaningful word of the model text, e.g. 'Maruti Swift VDI' -> 'swift'."""
    brand_words = set(str(brand).lower().replace("-", " ").split()) | _BRAND_WORDS
    for word in re.split(r"[^a-z0-9]+", str(model_text).lower()):
        if word and word not in brand_words:
            return word
    return "unknown"


def _common(records: pd.DataFrame, reference_year: int) -> pd.DataFrame:
    out = pd.DataFrame(index=records.index)
    out["brand"] = records["brand"].astype(str)
    out["model_name"] = [model_name(b, m) for b, m in zip(records["brand"], records["model"])]
    out["seller_type"] = records.get("seller_type", pd.Series("Individual", index=records.index)).fillna("Individual")
    out["age"] = (reference_year - pd.to_numeric(records["year"])).clip(lower=0)
    out["km_driven"] = pd.to_numeric(records["km_driven"])
    out["owner_rank"] = records["owners"].map(OWNER_RANK).fillna(1)
    return out


def car_features(records: pd.DataFrame, reference_year: int | None = None) -> pd.DataFrame:
    """Feature table for the car model."""
    out = _common(records, reference_year or current_year())
    out["fuel_type"] = records["fuel_type"].astype(str)
    # The dataset only distinguishes Manual vs Automatic.
    out["transmission"] = np.where(records["transmission"].astype(str) == "Manual", "Manual", "Automatic")
    out["engine_cc"] = pd.to_numeric(records.get("engine_cc"), errors="coerce").replace(0, np.nan)
    out["seats"] = pd.to_numeric(records.get("seats"), errors="coerce")
    return out[CAR_CATEGORICAL + CAR_NUMERIC]


def two_wheeler_features(records: pd.DataFrame, reference_year: int | None = None) -> pd.DataFrame:
    """Feature table for the shared scooter/bike model (``segment`` column required)."""
    out = _common(records, reference_year or current_year())
    out["segment"] = records["segment"].astype(str)
    price = pd.to_numeric(records.get("original_price"), errors="coerce").where(lambda p: p > 0)
    out["log_original_price"] = np.log(price)
    return out[TWO_WHEELER_CATEGORICAL + TWO_WHEELER_NUMERIC]
