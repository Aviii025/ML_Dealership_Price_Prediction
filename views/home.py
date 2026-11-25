"""Landing page for the dealership app."""

import streamlit as st

from src.storage import load_submissions
from src.theme import page_header

page_header(
    "Dealership Purchase Desk",
    "Fair offers for used cars, scooters & bikes.",
    "Enter what the seller brings in and get a data-driven purchase offer in seconds, "
    "priced by models trained on thousands of real listings.",
)

VEHICLES = (
    ("car", "🚗", "Cars", "Hatchbacks, sedans, SUVs and more.", "views/cars.py"),
    ("scooter", "🛵", "Scooters", "Petrol and electric scooters.", "views/scooters.py"),
    ("bike", "🏍️", "Bikes", "Commuters, cruisers and sports bikes.", "views/bikes.py"),
)

for col, (vtype, emoji, title, desc, page) in zip(st.columns(3, gap="medium"), VEHICLES):
    with col.container(key=f"vcard_{vtype}"):
        count = len(load_submissions(vtype))
        st.html(
            f'<div class="ui-vcard-emoji">{emoji}</div>'
            f'<div class="ui-vcard-title">{title}</div>'
            f'<p class="ui-vcard-desc">{desc}</p>'
            f'<div class="ui-vcard-count"><strong>{count}</strong> evaluation{"s" if count != 1 else ""} saved</div>'
        )
        st.page_link(page, label=f"Evaluate {title.lower()} →")

st.html(
    """
<div class="ui-steps">
  <div><span>01</span><h4>Enter the details</h4>
    <p>Seller info, the vehicle, its usage and condition.</p></div>
  <div><span>02</span><h4>Get an ML price</h4>
    <p>Trained models estimate the market value, then condition, insurance, accidents and
       documents adjust it. Electric vehicles use a rule-based estimate.</p></div>
  <div><span>03</span><h4>Save &amp; export</h4>
    <p>Every evaluation is saved and can be downloaded as CSV from its page.</p></div>
</div>
"""
)
