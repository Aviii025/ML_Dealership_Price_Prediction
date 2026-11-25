"""Input form for purchasing second-hand cars."""

import streamlit as st

from src import config
from src.components import (
    basic_vehicle_section, handle_submission, recent_submissions,
    seller_section, usage_condition_section,
)
from src.theme import page_header

VEHICLE = "car"

page_header("Cars", "What's the car worth?", "Fill in the car's details to get a suggested purchase offer.")

with st.form("car_form"):
    record = seller_section(VEHICLE)
    record.update(basic_vehicle_section(VEHICLE))

    st.subheader("Car specifications")
    c1, c2, c3 = st.columns(3)
    record["body_type"] = c1.selectbox("Body type", config.CAR_BODY_TYPES)
    record["transmission"] = c2.selectbox("Transmission", config.CAR_TRANSMISSIONS)
    record["engine_cc"] = c3.number_input("Engine capacity (cc)", min_value=0, max_value=8000, value=1200, step=100)
    c4, c5, c6 = st.columns(3)
    record["seats"] = c4.selectbox("Seats", (2, 4, 5, 6, 7, 8, 9), index=2)
    record["colour"] = c5.text_input("Colour")
    record["service_history"] = c6.selectbox("Service history", ("Authorised centre", "Local garage", "Unknown"))

    record.update(usage_condition_section(VEHICLE))
    submitted = st.form_submit_button("Evaluate car", type="primary", width="stretch")

if submitted:
    handle_submission(VEHICLE, record)

recent_submissions(VEHICLE)
