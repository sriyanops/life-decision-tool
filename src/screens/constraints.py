# src/screens/constraints.py
from __future__ import annotations

import streamlit as st

import nav
import state


def _helper(text: str) -> None:
    st.markdown(f"<div class='small-muted'>{text}</div>", unsafe_allow_html=True)


def render() -> None:
    d = state.get_decision()
    limits = d.limits

    # --- Header ---
    st.markdown("## Set your boundaries")
    _helper("You’re not judging what’s “good” — you’re deciding what you’re not willing to live with.")
    _helper("Your decision type helps the tool interpret these limits.")
    st.markdown("---")

    # --- 1) Money at risk (NUMERIC) ---
    st.markdown("### Money at risk")
    _helper("What’s the most money you’re willing to lose if this doesn’t work out? Include money spent or income you’d give up.")
    limits.money_max_usd = int(
        st.slider(
            "Max money at risk (USD)",
            min_value=0,
            max_value=20000,
            value=int(getattr(limits, "money_max_usd", 1000)),
            step=100,
            key="lim_money",
            label_visibility="collapsed",
        )
    )

    st.write("")

    # --- 2) Time you can realistically give ---
    st.markdown("### Time you can realistically give")
    _helper("How many hours per week can you commit without breaking other priorities?")
    limits.time_hours_per_week = int(
        st.slider(
            "Max hours per week",
            min_value=0,
            max_value=80,
            value=int(limits.time_hours_per_week),
            step=1,
            key="lim_time",
            label_visibility="collapsed",
        )
    )

    st.write("")

    # --- 3) Stress you can sustain ---
    st.markdown("### Stress you can sustain")
    _helper("What level of ongoing stress can you live with for months (not just a short push)?")
    limits.stress = state.risk_radio(
        "Stress tolerance",
        "lim_stress",
        limits.stress,
        label_visibility="collapsed",
    )

    st.write("")

    # --- 4) Impact on important relationships ---
    st.markdown("### Impact on important relationships")
    _helper("Would this seriously strain relationships that matter to you?")
    limits.relationships = state.risk_radio(
        "Relationship impact tolerance",
        "lim_rel",
        getattr(limits, "relationships", None),
        label_visibility="collapsed",
    )

    st.markdown("---")

    limits.confirmed = st.checkbox(
        "I’m comfortable removing any option that crosses these limits.",
        value=bool(limits.confirmed),
        key="lim_confirmed",
    )

    st.markdown("---")

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        if st.button("← Back", use_container_width=True):
            nav.set_page(nav.CATEGORY)

    with c2:
        if st.button("Lock my limits", use_container_width=True, disabled=not limits.confirmed):
            nav.set_page(nav.OPTIONS)
