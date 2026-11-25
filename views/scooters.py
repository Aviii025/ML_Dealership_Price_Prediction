"""Input form for purchasing second-hand scooters."""

import streamlit as st

from src import config
from src.components import (
    basic_vehicle_section, handle_submission, recent_submissions,
    seller_section, usage_condition_section,
)
from src.theme import page_header

VEHICLE = "scooter"

page_header("Scooters", "What's the scooter worth?", "Fill in the scooter's details to get a suggested purchase offer.")

with st.form("scooter_form"):
    record = seller_section(VEHICLE)
    record.update(basic_vehicle_section(VEHICLE))

    st.subheader("Scooter specifications")
    c1, c2, c3 = st.columns(3)
    record["engine_cc"] = c1.number_input(
        "Engine capacity (cc) — 0 for electric", min_value=0, max_value=400, value=110, step=5,
    )
    record["battery_kwh"] = c2.number_input(
        "Battery capacity (kWh) — electric only", min_value=0.0, max_value=10.0, value=0.0, step=0.1,
    )
    record["brake_type"] = c3.selectbox("Brakes", config.BRAKE_TYPES)
    c4, c5 = st.columns(2)
    record["colour"] = c4.text_input("Colour")
    record["tyre_condition"] = c5.selectbox("Tyre condition", ("New", "Good", "Needs replacement"))

    record.update(usage_condition_section(VEHICLE))
    submitted = st.form_submit_button("Evaluate scooter", type="primary", width="stretch")

if submitted:
    handle_submission(VEHICLE, record)

recent_submissions(VEHICLE)
