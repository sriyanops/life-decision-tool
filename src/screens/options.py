# src/screens/options.py
from __future__ import annotations

import streamlit as st

import nav
import state
from models import OptionInput


def _option_form(opt: OptionInput, prefix: str) -> None:
    st.markdown(f"### {opt.name}")
    st.write("")

    # ---- Money at risk (NUMERIC) ----
    st.markdown("#### Money at risk")
    st.markdown(
        "<div class='small-muted'>Worst case: how much money would realistically be on the line?</div>",
        unsafe_allow_html=True,
    )
    opt.money_at_risk_usd = int(
        st.slider(
            "Money at risk (USD)",
            min_value=0,
            max_value=20000,
            value=int(opt.money_at_risk_usd),
            step=100,
            key=f"{prefix}_money",
            label_visibility="collapsed",
        )
    )

    st.write("")

    # ---- Time Demand ----
    st.markdown("#### Time demand")
    st.markdown(
        "<div class='small-muted'>How much time would this option require weekly?</div>",
        unsafe_allow_html=True,
    )
    opt.time_required_hours_per_week = int(
        st.slider(
            "Hours per week required",
            min_value=0,
            max_value=80,
            value=int(opt.time_required_hours_per_week),
            step=1,
            key=f"{prefix}_time",
            label_visibility="collapsed",
        )
    )

    st.write("")

    # ---- Stress & Health Load ----
    st.markdown("#### Stress & health load")
    st.markdown(
        "<div class='small-muted'>What level of ongoing stress or health impact would this create?</div>",
        unsafe_allow_html=True,
    )
    opt.stress_fit = state.risk_radio(
        "Stress & health load",
        f"{prefix}_stress",
        opt.stress_fit,
        label_visibility="collapsed",
    )

    st.write("")

    # ---- Relationship Impact ----
    st.markdown("#### Impact on relationships")
    st.markdown(
        "<div class='small-muted'>How would this option affect the people you care about?</div>",
        unsafe_allow_html=True,
    )
    opt.relationships_impact = state.risk_radio(
        "Impact on relationships",
        f"{prefix}_rel",
        opt.relationships_impact,
        label_visibility="collapsed",
    )

    st.write("")

    # ---- Human grounding (non-scored) ----
    opt.summary = st.text_area(
        "Day-to-day changes (not scored)",
        value=opt.summary,
        placeholder="A few sentences. This isn’t scored — it’s here to keep you grounded in reality.",
        key=f"{prefix}_summary",
        height=120,
        label_visibility="visible",
    )


def render() -> None:
    d = state.get_decision()
    limits = d.limits
    opt_a, opt_b = state.get_options()

    st.markdown("## Describe your options")
    st.markdown(
        "<div class='small-muted'>Describe what each option would realistically require from you. Be honest — this is about reality, not optimism.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # ---- Option names ----
    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        opt_a.name = st.text_input(
            "Option A name",
            value=opt_a.name,
            key="opt_a_name",
            label_visibility="collapsed",
            placeholder="Option A name",
        )
    with c2:
        opt_b.name = st.text_input(
            "Option B name",
            value=opt_b.name,
            key="opt_b_name",
            label_visibility="collapsed",
            placeholder="Option B name",
        )

    st.markdown("---")

    # ---- Option forms ----
    left, right = st.columns([1, 1], gap="large")
    with left:
        _option_form(opt_a, "opt_a")
    with right:
        _option_form(opt_b, "opt_b")

    st.markdown("---")

    # ---- Gating ----
    a_name_ok = bool(opt_a.name.strip())
    b_name_ok = bool(opt_b.name.strip())
    limits_ok = bool(limits.confirmed)
    can_continue = limits_ok and a_name_ok and b_name_ok

    # ---- Navigation ----
    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        if st.button("← Edit limits", use_container_width=True):
            nav.set_page(nav.LIMITS)

    with c2:
        if st.button(
            "Compare my options",
            use_container_width=True,
            disabled=not can_continue,
        ):
            nav.set_page(nav.COMPARE)
