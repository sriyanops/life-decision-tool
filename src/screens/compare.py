# src/screens/compare.py
from __future__ import annotations

import streamlit as st

import nav
import state
from criteria import weighted_score
from models import check_limits


# STRICT-4 (v0.1) — these are the only enforced boundaries
CHECK_ORDER = [
    ("money", "Money at risk"),
    ("time", "Time demand"),
    ("stress", "Stress & health load"),
    ("relationships", "Impact on relationships"),
]


def _first_failure_key(checks: dict[str, bool]) -> str | None:
    for key, _label in CHECK_ORDER:
        if checks.get(key) is False:
            return key
    return None


def _fmt_usd(n: int) -> str:
    try:
        return f"${int(n):,}"
    except Exception:
        return "$0"


def _failure_explanation(key: str | None, limits, opt=None) -> str:
    if key is None:
        return "Fits within your boundaries."

    if key == "money":
        max_ok = int(getattr(limits, "money_max_usd", 0))
        opt_val = getattr(opt, "money_at_risk_usd", None) if opt is not None else None
        if opt_val is not None:
            return f"This risks {_fmt_usd(int(opt_val))}, which is above your limit ({_fmt_usd(int(max_ok))})."
        return f"This crosses the money risk you set ({_fmt_usd(int(max_ok))})."

    if key == "time":
        return f"This asks for more time than your limit ({int(limits.time_hours_per_week)} hrs/week)."

    if key == "stress":
        return "This creates more sustained stress than you said you can sustain."

    if key == "relationships":
        return "This risks straining important relationships beyond what you said you can accept."

    return "This crosses one of your boundaries."


def _render_boundary_card(title: str, checks: dict[str, bool], passed: bool, limits, opt) -> None:
    st.markdown(f"### {title}")

    rows = []
    for key, label in CHECK_ORDER:
        ok = checks.get(key, True)
        rows.append((label, "✅ Fits" if ok else "❌ Exceeds"))

    st.table(rows)

    if passed:
        st.success("Result: Fits within your boundaries.")
    else:
        fail_key = _first_failure_key(checks)
        st.error("Result: Removed")
        st.markdown(
            f"<div class='small-muted'>{_failure_explanation(fail_key, limits, opt)}</div>",
            unsafe_allow_html=True,
        )


def _final_context_block(
    *,
    opt,
    passed: bool,
    score: float | None,
) -> None:
    """
    End-of-page summary: fit + score + what actually changes day-to-day.
    """
    status = "✅ Fits" if passed else "❌ Removed"
    score_txt = f"{int(round(score))}" if (score is not None and passed) else "N/A"

    st.markdown(f"### {opt.name}")
    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown(f"**Status:** {status}")
    with c2:
        st.markdown(f"**Score:** {score_txt}")

    summary = (getattr(opt, "summary", "") or "").strip()
    if summary:
        st.markdown("**What would actually change day-to-day**")
        st.markdown(summary)
    else:
        st.markdown(
            "<div class='small-muted'>No day-to-day summary was entered on the Options page.</div>",
            unsafe_allow_html=True,
        )


def render() -> None:
    d = state.get_decision()
    limits = d.limits
    opt_a, opt_b = state.get_options()
    category = d.category or "Personal"

    st.markdown("## Compare your options")
    st.markdown(
        "<div class='small-muted'>First we remove what doesn’t fit your boundaries. Then we compare what’s left.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    if not limits.confirmed:
        st.warning("Limits aren’t locked yet.")
        if st.button("Go to limits →", use_container_width=True):
            nav.set_page(nav.LIMITS)
        return

    # 1) Boundary check
    st.markdown("### Boundary check")
    st.markdown("")

    a_checks = check_limits(limits, opt_a)
    b_checks = check_limits(limits, opt_b)

    a_pass = all(a_checks.values())
    b_pass = all(b_checks.values())

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        _render_boundary_card(opt_a.name, a_checks, a_pass, limits, opt_a)
    with c2:
        _render_boundary_card(opt_b.name, b_checks, b_pass, limits, opt_b)

    st.markdown("---")

    # Pre-compute scores (shown later in Results as N/A if removed)
    score_a = float(weighted_score(category, opt_a.criteria))
    score_b = float(weighted_score(category, opt_b.criteria))

    # Outcomes
    if a_pass and not b_pass:
        st.markdown("### Result")
        st.info(f"Only one option fits within your boundaries: **{opt_a.name}**.")
        st.markdown("---")

    elif b_pass and not a_pass:
        st.markdown("### Result")
        st.info(f"Only one option fits within your boundaries: **{opt_b.name}**.")
        st.markdown("---")

    elif not a_pass and not b_pass:
        st.markdown("### Result")
        st.error("Neither option fits within the boundaries you set.")
        st.markdown(
            "<div class='small-muted'>You may need to adjust your boundaries or rethink the options.</div>",
            unsafe_allow_html=True,
        )
        st.markdown("---")

    else:
        # 2) Category-based comparison
        st.markdown("### What matters most for this decision")
        st.markdown(
            f"<div class='small-muted'>Because this is a <b>{category}</b> decision, some trade-offs matter more than others.</div>",
            unsafe_allow_html=True,
        )
        st.markdown("")

        if score_a > score_b:
            st.markdown(f"**Based on what you set, {opt_a.name} fits better.**")
            st.markdown(
                f"""
- It aligns more strongly with what matters in **{category}** decisions.
- It stays within your boundaries while producing a better overall fit.
- It asks for trade-offs that you rated as more acceptable.
                """.strip()
            )
        elif score_b > score_a:
            st.markdown(f"**Based on what you set, {opt_b.name} fits better.**")
            st.markdown(
                f"""
- It aligns more strongly with what matters in **{category}** decisions.
- It stays within your boundaries while producing a better overall fit.
- It asks for trade-offs that you rated as more acceptable.
                """.strip()
            )
        else:
            st.markdown("**Based on what you set, this is a tie.**")
            st.markdown(
                """
- Both options fit within your boundaries.
- Your category criteria score them equally.
- The deciding factor is likely something outside the sliders (values, timing, gut-check).
                """.strip()
            )

        st.markdown("---")

    # ✅ End-of-page: results (fit/removed + score + day-to-day)
    st.markdown("## Results")
    st.markdown("")

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        _final_context_block(opt=opt_a, passed=a_pass, score=score_a if a_pass else None)
    with c2:
        _final_context_block(opt=opt_b, passed=b_pass, score=score_b if b_pass else None)

    st.markdown("---")

    # Navigation
    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        if st.button("← Edit options", use_container_width=True):
            nav.set_page(nav.OPTIONS)

    with c2:
        st.button("Export summary (coming soon)", use_container_width=True, disabled=True)
