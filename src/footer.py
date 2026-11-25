"""Site-wide footer shown below every page.

A blue card with large rounded top corners, a headline, link columns and
credits, with an oversized script "J" running off the top and bottom edges.
"""

import base64
from datetime import date

import streamlit as st

REPO_URL = "https://github.com/sjapanjots/ML_Dealership_Price_Prediction"
AUTHORS = ("Japanjot Singh", "Avinash Kumar")

BLUE = "#4B6BF5"
INK = "#0B0B0B"

# Streamlit's HTML sanitiser strips inline <svg>, so SVGs are embedded as <img> data URIs.
_SCRIPT_J_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 1000">'
    '<path d="M 90 360 C 40 220, 190 70, 400 60 C 590 52, 650 170, 560 235 '
    "C 460 300, 280 270, 290 175 C 300 90, 500 90, 520 230 "
    "C 535 420, 470 650, 380 810 C 320 915, 150 935, 110 850 "
    'C 75 770, 230 700, 390 735 C 470 752, 540 790, 600 840" '
    f'fill="none" stroke="{INK}" stroke-width="62" stroke-linecap="round" stroke-linejoin="round"/>'
    "</svg>"
)

_GITHUB_SVG = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="{INK}">'
    '<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49'
    "-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82"
    ".72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15"
    "-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04"
    " 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25"
    '.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>'
    "</svg>"
)


def _data_uri(svg: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


# (label, href, opens in new tab)
LINK_COLUMNS = (
    (("Cars", "cars", False), ("Scooters", "scooters", False), ("Bikes", "bikes", False)),
    (("How pricing works", f"{REPO_URL}#how-the-price-is-estimated", True),
     ("Model accuracy", f"{REPO_URL}#the-models", True),
     ("Datasets", f"{REPO_URL}#datasets", True)),
    (("Source code", REPO_URL, True),
     ("Report an issue", f"{REPO_URL}/issues", True),
     ("Retrain the models", f"{REPO_URL}#retraining", True)),
)

_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600&display=swap');

/* Let the footer sit flush with the bottom of the page. */
[data-testid="stMainBlockContainer"] {{ padding-bottom: 0 !important; }}
/* Measure the main area (everything right of the sidebar) so the footer can span it edge to edge. */
[data-testid="stMain"] {{ container-type: inline-size; }}

.jf {{
  --jf-blue: {BLUE};
  --jf-ink: {INK};
  /* Content gutter: matches the page's side padding, centred when the page hits its max width. */
  --jf-gutter: max(5rem, calc((100cqw - 1180px) / 2 + 5rem));
  position: relative;
  width: 100cqw;                         /* full width of the main area, no side gaps */
  margin-left: calc(50% - 50cqw);
  margin-top: 5rem;
  padding-top: 110px;           /* room for the J to rise above the card */
  overflow: hidden;             /* clip the J at the bottom of the card */
  font-family: 'Figtree', 'Source Sans Pro', sans-serif;
  color: var(--jf-ink);
}}
.jf__card {{
  position: relative;
  background: var(--jf-blue);
  border-radius: 56px 56px 0 0;
  padding: 3.5rem var(--jf-gutter) 2rem;
  min-height: 520px;
  display: flex; flex-direction: column;
}}
.jf__letter {{
  position: absolute;
  z-index: 1;
  right: calc(var(--jf-gutter) - 2rem);
  top: 0;
  height: calc(100% + 60px);    /* rises above the card and runs off the bottom, clipped by .jf */
  width: auto;
  pointer-events: none;
  user-select: none;
}}
.jf__content {{ position: relative; z-index: 2; max-width: 52%; display: flex; flex-direction: column; flex: 1; }}
.jf__kicker {{ font-size: 1.15rem; margin: 0 0 .4rem; }}
.jf__headline {{
  font-size: clamp(2.2rem, 4.2vw, 4rem);
  font-weight: 500; line-height: 1.02; letter-spacing: -0.035em;
  margin: 0;
}}
.jf__headline a {{ color: inherit; text-decoration: none; }}
.jf__headline a:hover {{ text-decoration: underline; text-decoration-thickness: 3px; text-underline-offset: 8px; }}
.jf__spacer {{ flex: 1; min-height: 3rem; }}
.jf__links {{ display: grid; grid-template-columns: repeat(3, max-content); gap: .55rem 3.5rem; }}
.jf__col {{ display: flex; flex-direction: column; gap: .55rem; }}
.jf a.jf__link {{ color: var(--jf-ink); text-decoration: none; font-size: 1.12rem; width: fit-content; }}
.jf a.jf__link:hover {{ text-decoration: underline; text-underline-offset: 4px; }}
.jf__social {{ margin: 2.2rem 0 1.4rem; display: flex; gap: 1rem; }}
.jf__social a {{ display: inline-flex; transition: transform .2s ease; }}
.jf__social a:hover {{ transform: translateY(-2px); }}
.jf__legal {{ display: flex; flex-wrap: wrap; gap: .4rem 1.4rem; font-size: .9rem; }}
.jf__legal a {{ color: var(--jf-ink); text-decoration: none; }}
.jf__legal a:hover {{ text-decoration: underline; }}
.jf__legal strong {{ font-weight: 600; white-space: nowrap; }}

@media (max-width: 900px) {{
  .jf {{ padding-top: 70px; --jf-gutter: 1rem; }}
  .jf__card {{ border-radius: 40px 40px 0 0; padding: 2.5rem var(--jf-gutter) 1.6rem; min-height: 0; }}
  /* Keep the J in the top-right corner, beside the headline and above the links. */
  .jf__letter {{ height: 250px; right: -10px; }}
  .jf__content {{ max-width: 100%; }}
  .jf__kicker {{ font-size: 1rem; max-width: 52%; }}
  .jf__headline {{ font-size: 2.1rem; max-width: 52%; }}
  .jf__spacer {{ min-height: 2.5rem; }}
  .jf__links {{ grid-template-columns: 1fr 1fr; gap: .55rem 1.5rem; }}
  .jf a.jf__link {{ font-size: 1rem; }}
}}
</style>
"""


def _links_html() -> str:
    cols = []
    for column in LINK_COLUMNS:
        items = "".join(
            f'<a class="jf__link" href="{href}" '
            + ('target="_blank" rel="noopener noreferrer"' if new_tab else 'target="_self"')
            + f">{label}</a>"
            for label, href, new_tab in column
        )
        cols.append(f'<div class="jf__col">{items}</div>')
    return "".join(cols)


def render_footer() -> None:
    """Render the blue footer with the script J, links and credits."""
    credits = " &amp; ".join(f"<strong>{name}</strong>" for name in AUTHORS)
    st.html(
        _CSS
        + f"""
<footer class="jf">
  <div class="jf__card">
    <div class="jf__content">
      <p class="jf__kicker">Got a car, scooter or bike to sell?</p>
      <p class="jf__headline"><a href="cars" target="_self">Get a fair offer today.</a></p>
      <div class="jf__spacer"></div>
      <nav class="jf__links" aria-label="Footer">{_links_html()}</nav>
      <div class="jf__social">
        <a href="{REPO_URL}" target="_blank" rel="noopener noreferrer" aria-label="GitHub repository">
          <img src="{_data_uri(_GITHUB_SVG)}" width="28" height="28" alt="GitHub" />
        </a>
      </div>
      <div class="jf__legal">
        <span>© {date.today().year} Coded, designed &amp; developed by {credits}</span>
        <a href="{REPO_URL}" target="_blank" rel="noopener noreferrer">GitHub</a>
        <span>Built with Streamlit</span>
      </div>
    </div>
  </div>
</footer>
"""
    )
