"""Load the raw datasets and convert them to the app's record format."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import BRANDS

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

# Both datasets were scraped in 2020; ages are measured from this year.
DATA_REFERENCE_YEAR = 2020

CAR_OWNERS = {
    "First Owner": "1st Owner", "Second Owner": "2nd Owner",
    "Third Owner": "3rd Owner", "Fourth & Above Owner": "4th Owner or more",
}
CAR_BRAND_ALIASES = {"Maruti": "Maruti Suzuki", "Land": "Land Rover"}

TWO_WHEELER_OWNERS = {
    "1st owner": "1st Owner", "2nd owner": "2nd Owner",
    "3rd owner": "3rd Owner", "4th owner": "4th Owner or more",
}
TWO_WHEELER_BRAND_ALIASES = {"Royal": "Royal Enfield", "Harley": "Harley-Davidson", "Activa": "Honda"}

# Model names that identify a scooter (everything else is treated as a motorcycle).
SCOOTER_KEYWORDS = (
    "activa", "access", "maestro", "dio", "scooty", "aviator", "pleasure", "duet",
    "wego", "fascino", "navi", "jupiter", "ntorq", "vespa", "ray", "zest", "pep",
    "grazia", "burgman", "destini", "swish", "lets", "alpha", "cliq", "style",
)


def load_cars() -> pd.DataFrame:
    """CarDekho used-car listings -> app records with a ``price`` target."""
    raw = pd.read_csv(RAW_DIR / "cars_cardekho.csv").drop_duplicates()
    raw = raw[raw["owner"].isin(CAR_OWNERS)]  # drops 'Test Drive Car'
    first_word = raw["name"].str.split().str[0]
    brand = first_word.replace(CAR_BRAND_ALIASES)
    return pd.DataFrame({
        "brand": brand.where(brand.isin(BRANDS["car"]), "Other"),
        "model": raw["name"].str.split(n=1).str[1],
        "year": raw["year"],
        "km_driven": raw["km_driven"],
        "owners": raw["owner"].map(CAR_OWNERS),
        "fuel_type": raw["fuel"],
        "transmission": raw["transmission"],
        "seller_type": raw["seller_type"].replace({"Trustmark Dealer": "Dealer"}),
        "engine_cc": pd.to_numeric(raw["engine"].str.extract(r"(\d+)")[0], errors="coerce"),
        "seats": raw["seats"],
        "price": raw["selling_price"],
    }).reset_index(drop=True)


def is_scooter(model_text: str) -> bool:
    words = set(str(model_text).lower().split())
    return any(k in words for k in SCOOTER_KEYWORDS)


def load_two_wheelers() -> pd.DataFrame:
    """Used motorcycle/scooter listings -> app records with ``segment`` and ``price``."""
    raw = pd.read_csv(RAW_DIR / "two_wheelers.csv").drop_duplicates()
    raw = raw[raw["Owner"].isin(TWO_WHEELER_OWNERS)]
    brand = raw["Brand"].replace(TWO_WHEELER_BRAND_ALIASES)
    known = set(BRANDS["bike"]) | set(BRANDS["scooter"])
    return pd.DataFrame({
        "segment": ["scooter" if is_scooter(m) else "bike" for m in raw["Model"]],
        "brand": brand.where(brand.isin(known), "Other"),
        "model": raw["Model"],
        "year": raw["Year"],
        "km_driven": raw["KM_Driven"],
        "owners": raw["Owner"].map(TWO_WHEELER_OWNERS),
        "seller_type": raw["Seller_Type"],
        "original_price": raw["Ex_Showroom_Price"],
        "price": raw["Selling_Price"],
    }).reset_index(drop=True)
