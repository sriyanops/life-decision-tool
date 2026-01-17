# src/screens/category.py
from __future__ import annotations

import streamlit as st

import nav
import state
from models import DEFAULT_CATEGORIES


def render() -> None:
    d = state.get_decision()

    st.markdown("## Start a decision")
    st.markdown(
        "<div class='small-muted'>You’re not judging what’s “good” — you’re deciding what you’re not willing to live with.</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='small-muted'>Your decision type helps the tool interpret your limits.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    d.title = st.text_input(
        "Decision title",
        value=d.title,
        placeholder="e.g., Take the IT helpdesk offer or keep building certs/labs",
    )

    st.markdown("### Decision type")
    cat_default = d.category if d.category in DEFAULT_CATEGORIES else DEFAULT_CATEGORIES[0]
    d.category = st.radio(
        "Decision type",
        DEFAULT_CATEGORIES,
        index=DEFAULT_CATEGORIES.index(cat_default),
        horizontal=True,
        label_visibility="collapsed",
    )

    st.markdown("---")

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        if st.button("← Back", use_container_width=True):
            nav.set_page(nav.HOME)

    with c2:
        disabled = not d.title.strip()
        if st.button("Next → Limits", use_container_width=True, disabled=disabled):
            nav.set_page(nav.LIMITS)
