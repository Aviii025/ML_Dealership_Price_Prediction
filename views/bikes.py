"""Input form for purchasing second-hand motorcycles."""

import streamlit as st

from src import config
from src.components import (
    basic_vehicle_section, handle_submission, recent_submissions,
    seller_section, usage_condition_section,
)
from src.theme import page_header

VEHICLE = "bike"

page_header("Bikes", "What's the bike worth?", "Fill in the motorcycle's details to get a suggested purchase offer.")

with st.form("bike_form"):
    record = seller_section(VEHICLE)
    record.update(basic_vehicle_section(VEHICLE))

    st.subheader("Bike specifications")
    c1, c2, c3 = st.columns(3)
    record["bike_type"] = c1.selectbox("Bike type", config.BIKE_TYPES)
    record["engine_cc"] = c2.number_input("Engine capacity (cc)", min_value=0, max_value=2500, value=150, step=5)
    record["brake_type"] = c3.selectbox("Brakes", config.BRAKE_TYPES)
    c4, c5, c6 = st.columns(3)
    record["gears"] = c4.number_input("Number of gears", min_value=0, max_value=7, value=5)
    record["colour"] = c5.text_input("Colour")
    record["modified"] = c6.toggle("Aftermarket modifications?")

    record.update(usage_condition_section(VEHICLE))
    submitted = st.form_submit_button("Evaluate bike", type="primary", width="stretch")

if submitted:
    handle_submission(VEHICLE, record)

recent_submissions(VEHICLE)
