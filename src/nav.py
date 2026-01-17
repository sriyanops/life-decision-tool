# src/nav.py
from __future__ import annotations

import streamlit as st

# Canonical page names (must match app.py PAGES)
HOME = "Home"
CATEGORY = "Category"
LIMITS = "Limits"
OPTIONS = "Options"
COMPARE = "Compare"
PAST = "Past Decisions"
LOAD = "Load Decision"

ALL_PAGES = [HOME, CATEGORY, LIMITS, OPTIONS, COMPARE, PAST, LOAD]


def get_page() -> str:
    page = st.session_state.get("page", HOME)
    return page if page in ALL_PAGES else HOME


def set_page(name: str) -> None:
    """
    Single source of truth for navigation.

    Rules:
    - Updates st.session_state.page (used by app.py to render)
    - Does NOT touch nav_radio (Streamlit can error if you mutate a widget key after instantiation)
    - ONLY reruns if the page is actually changing (prevents rerun loops / janky sidebar behavior)
    """
    if name not in ALL_PAGES:
        raise ValueError(f"Unknown page '{name}'. Must be one of: {ALL_PAGES}")

    current = get_page()
    if name == current:
        return

    st.session_state.page = name
    st.rerun()


def goto_next() -> None:
    cur = get_page()
    i = ALL_PAGES.index(cur)
    if i < len(ALL_PAGES) - 1:
        set_page(ALL_PAGES[i + 1])


def goto_prev() -> None:
    cur = get_page()
    i = ALL_PAGES.index(cur)
    if i > 0:
        set_page(ALL_PAGES[i - 1])
