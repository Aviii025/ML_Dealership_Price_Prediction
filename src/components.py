"""Reusable Streamlit form sections shared by the car, scooter and bike pages."""

from __future__ import annotations

import re

import streamlit as st

from src import config
from src.storage import load_submissions, save_submission
from src.theme import result_card
from src.valuation import Valuation, estimate_price

PHONE_RE = re.compile(r"^\+?\d{10,13}$")


def format_inr(amount: float) -> str:
    """Format a number as Indian Rupees with lakh/crore digit grouping."""
    whole = str(int(round(amount)))
    if len(whole) > 3:
        head, tail = whole[:-3], whole[-3:]
        head = ",".join(re.findall(r"\d{1,2}", head[::-1]))[::-1]
        whole = f"{head},{tail}"
    return f"₹{whole}"


def seller_section(prefix: str) -> dict:
    """Seller contact details."""
    st.subheader("Seller details")
    c1, c2, c3 = st.columns(3)
    return {
        "seller_name": c1.text_input("Full name", key=f"{prefix}_name"),
        "seller_phone": c2.text_input("Phone number", key=f"{prefix}_phone", placeholder="+919876543210"),
        "seller_city": c3.text_input("City", key=f"{prefix}_city"),
    }


def basic_vehicle_section(vehicle_type: str) -> dict:
    """Brand, model, year, fuel, registration and original price."""
    st.subheader("Vehicle details")
    c1, c2, c3 = st.columns(3)
    details = {
        "brand": c1.selectbox("Brand", config.BRANDS[vehicle_type], key=f"{vehicle_type}_brand"),
        "model": c2.text_input("Model / variant", key=f"{vehicle_type}_model"),
        "year": c3.number_input(
            "Year of manufacture", min_value=config.MIN_YEAR, max_value=config.current_year(),
            value=config.current_year() - 3, step=1, key=f"{vehicle_type}_year",
        ),
    }
    c4, c5, c6 = st.columns(3)
    details["fuel_type"] = c4.selectbox("Fuel type", config.FUEL_TYPES[vehicle_type], key=f"{vehicle_type}_fuel")
    details["registration_number"] = c5.text_input(
        "Registration number", key=f"{vehicle_type}_reg", placeholder="e.g. PB10AB1234",
    ).upper().replace(" ", "")
    details["original_price"] = c6.number_input(
        "Original ex-showroom price (₹)", min_value=0, value=0, step=1000, key=f"{vehicle_type}_price",
    )
    return details


def usage_condition_section(vehicle_type: str) -> dict:
    """Odometer, ownership, condition, insurance, accident and documents."""
    st.subheader("Usage & condition")
    c1, c2, c3 = st.columns(3)
    details = {
        "km_driven": c1.number_input("Kilometres driven", min_value=0, value=0, step=500, key=f"{vehicle_type}_km"),
        "owners": c2.selectbox("Ownership", config.OWNER_OPTIONS, key=f"{vehicle_type}_owners"),
        "condition": c3.select_slider(
            "Overall condition", options=config.CONDITIONS[::-1], value="Good", key=f"{vehicle_type}_cond",
        ),
    }
    c4, c5, c6 = st.columns(3)
    details["insurance"] = c4.selectbox("Insurance", config.INSURANCE_OPTIONS, key=f"{vehicle_type}_ins")
    details["accident_history"] = c5.toggle("Any accident history?", key=f"{vehicle_type}_acc")
    details["documents_complete"] = c6.toggle(
        "RC & service records available", value=True, key=f"{vehicle_type}_docs",
    )
    details["remarks"] = st.text_area(
        "Remarks (scratches, repairs, modifications…)", key=f"{vehicle_type}_remarks",
    )
    return details


def validate(record: dict) -> list[str]:
    """Return a list of human-readable validation errors."""
    errors = []
    if not record.get("seller_name", "").strip():
        errors.append("Seller name is required.")
    if not PHONE_RE.match(record.get("seller_phone", "").replace(" ", "")):
        errors.append("Enter a valid phone number (10–13 digits).")
    if not record.get("model", "").strip():
        errors.append("Model / variant is required.")
    if not record.get("registration_number"):
        errors.append("Registration number is required.")
    if record.get("original_price", 0) <= 0:
        errors.append("Original price must be greater than zero.")
    return errors


def show_valuation(valuation: Valuation) -> None:
    """Render the estimated market value and the dealer's offer range."""
    st.toast("Evaluation saved.", icon="✅")
    result_card(
        offer=f"{format_inr(valuation.offer_low)} – {format_inr(valuation.offer_high)}",
        market_value=format_inr(valuation.market_value),
        source=valuation.source,
    )
    for note in valuation.notes:
        st.warning(note)


def handle_submission(vehicle_type: str, record: dict) -> None:
    """Validate, value and persist a submitted form."""
    errors = validate(record)
    if errors:
        for err in errors:
            st.error(err)
        return
    valuation = estimate_price(vehicle_type, record)
    save_submission(vehicle_type, {
        **record,
        "estimated_market_value": valuation.market_value,
        "offer_low": valuation.offer_low,
        "offer_high": valuation.offer_high,
        "valuation_source": valuation.source,
    })
    show_valuation(valuation)


def recent_submissions(vehicle_type: str, limit: int = 10) -> None:
    """Show the latest saved evaluations for this vehicle type."""
    df = load_submissions(vehicle_type)
    with st.expander(f"Recent {vehicle_type} evaluations ({len(df)})"):
        if df.empty:
            st.info("No evaluations saved yet.")
        else:
            st.dataframe(df.tail(limit).iloc[::-1], width="stretch", hide_index=True)
            st.download_button(
                f"Download all {vehicle_type} evaluations (CSV)",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name=f"{vehicle_type}_evaluations.csv",
                mime="text/csv",
                key=f"{vehicle_type}_download",
            )
            st.caption("Saved data is not permanent on Streamlit Cloud. Download it regularly.")
