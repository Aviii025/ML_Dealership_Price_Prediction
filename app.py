"""Entry point: `streamlit run app.py`."""

import streamlit as st

from src.footer import render_footer
from src.theme import apply_theme

st.set_page_config(page_title="Dealership Purchase Desk", page_icon="🚘", layout="wide")

pages = [
    st.Page("views/home.py", title="Home", icon="🏠", default=True),
    st.Page("views/cars.py", title="Cars", icon="🚗"),
    st.Page("views/scooters.py", title="Scooters", icon="🛵"),
    st.Page("views/bikes.py", title="Bikes", icon="🏍️"),
]

apply_theme()
st.navigation(pages).run()
render_footer()
