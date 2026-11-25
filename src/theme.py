"""Global look and feel, matching the footer's design.

Colours and fonts come from ``.streamlit/config.toml``. This module adds the
CSS the theme options can't express, plus small HTML building blocks used by
the pages (page header, result card).
"""

from __future__ import annotations

import html

import streamlit as st

BLUE = "#4B6BF5"
INK = "#0B0B0B"
PAPER = "#FCFBF7"
LINE = "#E4E1D8"

_CSS = f"""
<style>
/* ---------- type ---------- */
h1, h2, h3 {{ letter-spacing: -0.025em; }}
[data-testid="stMainBlockContainer"] {{ padding-top: 3rem; max-width: 1180px; }}

/* ---------- page header ---------- */
.ui-kicker {{
  display: inline-flex; align-items: center; gap: .5rem;
  font-size: .95rem; font-weight: 500; margin-bottom: .6rem;
}}
.ui-kicker::before {{
  content: ""; width: .7rem; height: .7rem; border-radius: 999px; background: {BLUE};
}}
.ui-title {{
  font-size: clamp(2.4rem, 5.2vw, 4.2rem); font-weight: 500;
  line-height: 1.02; letter-spacing: -0.04em; margin: 0 0 1rem; color: {INK};
}}
.ui-sub {{ font-size: 1.15rem; max-width: 46rem; color: #3b3b3b; margin: 0 0 1.5rem; }}

/* ---------- cards: forms, bordered containers, expanders ---------- */
[data-testid="stForm"] {{
  background: #fff; border: 1px solid {LINE}; border-radius: 32px; padding: 2.2rem 2.2rem 1.6rem;
}}
[data-testid="stForm"] h3 {{
  font-size: 1.15rem; font-weight: 600; letter-spacing: 0; margin-top: .6rem;
  padding-top: 1.2rem; border-top: 1px solid {LINE};
}}
[data-testid="stForm"] [data-testid="stVerticalBlock"] > div:first-child h3 {{ border-top: 0; padding-top: 0; }}
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]),
div[class*="st-key-vcard_"] {{ border-radius: 28px !important; }}
[data-testid="stExpander"] details {{ border-radius: 22px; background: #fff; }}
[data-testid="stAlert"] > div {{ border-radius: 18px; }}

/* ---------- buttons: black pill, blue on hover ---------- */
[data-testid^="stBaseButton-primary"] {{
  background: {INK} !important; border-color: {INK} !important; color: #fff !important;
  font-weight: 600; min-height: 3.2rem; font-size: 1.05rem;
  transition: background .2s ease, color .2s ease, transform .2s ease;
}}
[data-testid^="stBaseButton-primary"]:hover {{
  background: {BLUE} !important; border-color: {BLUE} !important; color: {INK} !important;
  transform: translateY(-1px);
}}
[data-testid="stDownloadButton"] button {{ border-radius: 999px; }}

/* ---------- sidebar navigation: pills, active page in blue ---------- */
[data-testid="stSidebarNav"] a {{ border-radius: 999px; padding: .45rem .9rem; margin-bottom: .2rem; }}
[data-testid="stSidebarNav"] a span {{ font-size: 1rem; color: {INK}; }}
[data-testid="stSidebarNav"] a[aria-current="page"] {{ background: {BLUE}; }}
[data-testid="stSidebarNav"] a[aria-current="page"] span {{ font-weight: 600; }}
[data-testid="stSidebarNav"] a:hover:not([aria-current="page"]) {{ background: #E8E5DC; }}

/* ---------- home: vehicle cards ---------- */
div[class*="st-key-vcard_"] {{
  background: #fff; padding: 1.6rem 1.6rem 1.2rem !important; border: 1px solid {LINE};
  transition: transform .2s ease, box-shadow .2s ease;
}}
div[class*="st-key-vcard_"]:hover {{ transform: translateY(-4px); box-shadow: 0 18px 40px rgba(11,11,11,.08); }}
.ui-vcard-emoji {{ font-size: 2.6rem; line-height: 1; }}
.ui-vcard-title {{ font-size: 1.7rem; font-weight: 600; letter-spacing: -0.02em; margin: .8rem 0 .2rem; }}
.ui-vcard-desc {{ color: #4a4a4a; margin: 0 0 1rem; min-height: 3.2em; }}  /* two lines, so cards align */
.ui-vcard-count {{ font-size: .9rem; color: #4a4a4a; }}
.ui-vcard-count strong {{ color: {INK}; font-size: 1.1rem; }}
div[class*="st-key-vcard_"] [data-testid="stPageLink"] a {{
  background: {INK}; border-radius: 999px; padding: .55rem 1.1rem; width: fit-content;
}}
div[class*="st-key-vcard_"] [data-testid="stPageLink"] a span,
div[class*="st-key-vcard_"] [data-testid="stPageLink"] a p {{ color: #fff !important; font-weight: 600; }}
div[class*="st-key-vcard_"] [data-testid="stPageLink"] a:hover {{ background: {BLUE}; }}
div[class*="st-key-vcard_"] [data-testid="stPageLink"] a:hover p {{ color: {INK} !important; }}

/* ---------- home: how it works ---------- */
.ui-steps {{
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem;
  margin-top: 2.5rem; padding-top: 2rem; border-top: 1px solid {LINE};
}}
.ui-steps span {{ font-size: .9rem; font-weight: 600; color: {BLUE}; }}
.ui-steps h4 {{ font-size: 1.25rem; font-weight: 600; margin: .4rem 0 .4rem; letter-spacing: -0.01em; }}
.ui-steps p {{ margin: 0; color: #4a4a4a; }}

/* ---------- result card ---------- */
.ui-result {{
  background: {BLUE}; color: {INK}; border-radius: 32px; padding: 2rem 2.2rem; margin: 1rem 0 .6rem;
  display: grid; grid-template-columns: minmax(0, 2fr) minmax(0, 1fr); gap: 1.5rem 2rem; align-items: end;
}}
.ui-result__label {{ font-size: 1rem; font-weight: 500; margin: 0 0 .3rem; }}
.ui-result__offer {{ white-space: nowrap; font-size: clamp(1.9rem, 3.4vw, 3rem); font-weight: 500; letter-spacing: -0.035em; line-height: 1.05; margin: 0; }}
.ui-result__value {{ font-size: 1.6rem; font-weight: 500; letter-spacing: -0.02em; margin: 0; }}
.ui-result__source {{ grid-column: 1 / -1; font-size: .9rem; margin: 0; padding-top: 1rem; border-top: 1px solid rgba(11,11,11,.2); }}
@media (max-width: 700px) {{
  [data-testid="stMainBlockContainer"] {{ padding-top: 4.5rem; }}  /* clear the mobile header bar */
  [data-testid="stForm"] {{ padding: 1.4rem 1.1rem 1rem; border-radius: 24px; }}
  .ui-steps {{ grid-template-columns: 1fr; gap: 1.4rem; }}
  .ui-result__offer {{ white-space: normal; }}
  .ui-result {{ grid-template-columns: 1fr; padding: 1.6rem 1.4rem; border-radius: 26px; }}
}}
</style>
"""


def apply_theme() -> None:
    """Inject the global CSS. Call once per run, before the page renders."""
    st.html(_CSS)


def page_header(kicker: str, title: str, subtitle: str = "") -> None:
    """Large editorial page header: coloured-dot kicker, big title, optional subtitle."""
    sub = f'<p class="ui-sub">{html.escape(subtitle)}</p>' if subtitle else ""
    st.html(
        f'<div class="ui-kicker">{html.escape(kicker)}</div>'
        f'<h1 class="ui-title">{html.escape(title)}</h1>{sub}'
    )


def result_card(offer: str, market_value: str, source: str) -> None:
    """Blue card showing the suggested offer and market value."""
    st.html(
        f"""
<div class="ui-result">
  <div>
    <p class="ui-result__label">Suggested purchase offer</p>
    <p class="ui-result__offer">{html.escape(offer)}</p>
  </div>
  <div>
    <p class="ui-result__label">Estimated market value</p>
    <p class="ui-result__value">{html.escape(market_value)}</p>
  </div>
  <p class="ui-result__source">Source: {html.escape(source)}</p>
</div>
"""
    )
