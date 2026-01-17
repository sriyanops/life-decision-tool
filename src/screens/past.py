# src/screens/past.py
from __future__ import annotations

import json
from datetime import datetime

import streamlit as st

import nav
import state


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def render() -> None:
    st.markdown("## Past Decisions")
    st.markdown(
        "<div class='small-muted'>Download your current decision as JSON. You can load it later from the Load page.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        if st.button("← Back to Home", use_container_width=True):
            nav.set_page(nav.HOME)
    with c2:
        if st.button("Go to Load →", use_container_width=True):
            nav.set_page(nav.LOAD)

    st.markdown("")

    snap = state.snapshot_current()
    data = json.dumps(snap, indent=2)

    st.download_button(
        "Download current decision (JSON)",
        data=data,
        file_name=f"life_decision_{_stamp()}.json",
        mime="application/json",
        use_container_width=True,
    )

    st.markdown("---")
    st.markdown("<div class='small-muted'>Preview</div>", unsafe_allow_html=True)
    st.code(data, language="json")
