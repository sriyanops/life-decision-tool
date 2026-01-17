# src/screens/load.py
from __future__ import annotations

import json
from typing import Any, Dict

import streamlit as st

import nav
import state


def _parse_json_text(raw: str) -> Dict[str, Any]:
    raw = raw.strip()
    if not raw:
        raise ValueError("Empty input.")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object (dictionary).")
    return data


def _try_apply_snapshot(snap: Dict[str, Any]) -> bool:
    """
    Returns True if applied successfully.
    We intentionally guard this so the screen never hard-crashes
    even if state.apply_snapshot() isn't implemented yet.
    """
    if not hasattr(state, "apply_snapshot"):
        st.error(
            "Load is wired, but state.apply_snapshot() is missing. "
            "Next step is updating src/state.py to implement it."
        )
        st.stop()

    try:
        # state.apply_snapshot should validate + normalize the structure
        state.apply_snapshot(snap)  # type: ignore[attr-defined]
        return True
    except Exception as e:
        st.error(f"Could not apply snapshot. ({e})")
        return False


def render() -> None:
    st.markdown("## Load saved decision")
    st.markdown(
        "<div class='small-muted'>Upload a decision JSON (exported from Past Decisions) or paste one below.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        if st.button("← Back", use_container_width=True):
            nav.set_page(nav.HOME)

    with c2:
        # keep right side open for future (e.g., help tooltip)
        st.markdown("")

    st.markdown("### Upload JSON")
    up = st.file_uploader("Decision JSON", type=["json"], label_visibility="collapsed")

    if up is not None:
        try:
            raw = up.read()
            # tolerate utf-8-sig BOM and typical encodings
            text = raw.decode("utf-8-sig")
            snap = _parse_json_text(text)

            # Optional quick preview (safe)
            title = str(snap.get("title", "")).strip()
            category = str(snap.get("category", "")).strip()
            if title or category:
                st.markdown(
                    f"<div class='small-muted'>Detected: <b>{title or 'Untitled'}</b>"
                    f"{(' — ' + category) if category else ''}</div>",
                    unsafe_allow_html=True,
                )

            if _try_apply_snapshot(snap):
                st.success("Loaded. Redirecting…")
                nav.set_page(nav.CATEGORY)

        except Exception as e:
            st.error(f"Could not load that file. ({e})")

    st.markdown("---")
    st.markdown("### Paste JSON")
    txt = st.text_area(
        "Paste JSON",
        height=200,
        placeholder='{"title":"...", "category":"...", "limits":{...}, "opt_a":{...}, "opt_b":{...}}',
        label_visibility="collapsed",
    )

    c3, c4 = st.columns([1, 1], gap="large")
    with c3:
        load_disabled = not txt.strip()
        if st.button("Load pasted JSON", use_container_width=True, disabled=load_disabled):
            try:
                snap = _parse_json_text(txt)
                if _try_apply_snapshot(snap):
                    st.success("Loaded. Redirecting…")
                    nav.set_page(nav.CATEGORY)
            except Exception as e:
                st.error(f"Could not parse JSON. ({e})")

    with c4:
        if st.button("Clear", use_container_width=True, disabled=not txt.strip()):
            st.session_state["load_paste_clear"] = True
            st.rerun()
