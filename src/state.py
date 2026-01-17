# src/state.py
from __future__ import annotations

import json
import re
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from models import Decision, Limits, OptionInput, Risk

# -----------------------------
# Persistence config
# -----------------------------
# Saves will land at: <project_root>/data/saved_decisions/*.json
# Works locally + Streamlit Community Cloud (note: cloud storage may be ephemeral on redeploy).
ROOT = Path(__file__).resolve().parents[1]
SAVE_DIR = ROOT / "data" / "saved_decisions"


def init_state() -> None:
    # navigation
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    # core decision object
    if "decision" not in st.session_state:
        st.session_state.decision = Decision()

    # options
    if "opt_a" not in st.session_state:
        st.session_state.opt_a = OptionInput(name="Option A")
    if "opt_b" not in st.session_state:
        st.session_state.opt_b = OptionInput(name="Option B")


def get_decision() -> Decision:
    return st.session_state.decision


def get_limits() -> Limits:
    return st.session_state.decision.limits


def get_options() -> tuple[OptionInput, OptionInput]:
    return st.session_state.opt_a, st.session_state.opt_b


# -----------------------------
# Snapshot helpers
# -----------------------------
def _risk_from_value(v: str | None) -> Risk:
    if not v:
        return Risk.MEDIUM
    for r in Risk:
        if r.value == v:
            return r
    return Risk.MEDIUM


def _safe_int(v: Any, default: int) -> int:
    try:
        return int(v)
    except Exception:
        return default


def snapshot_current() -> dict:
    """
    Serialize current session state into a JSON-safe snapshot.
    """
    d = get_decision()
    opt_a, opt_b = get_options()
    lim = d.limits

    # Ensure criteria is JSON-safe {str:int}
    def _criteria_safe(c: Any) -> dict[str, int]:
        if not isinstance(c, dict):
            return {}
        out: dict[str, int] = {}
        for k, v in c.items():
            if k is None:
                continue
            out[str(k)] = _safe_int(v, 0)
        return out

    return {
        "version": "0.1",
        "saved_at": datetime.now().isoformat(timespec="seconds"),
        "decision": {
            "title": d.title,
            "category": d.category,
            "limits": {
                "money_max_usd": _safe_int(getattr(lim, "money_max_usd", 1000), 1000),
                "time_hours_per_week": _safe_int(getattr(lim, "time_hours_per_week", 10), 10),
                "stress": getattr(lim.stress, "value", "Medium"),
                "relationships": getattr(lim.relationships, "value", "Medium"),
                "confirmed": bool(getattr(lim, "confirmed", False)),
            },
        },
        "options": {
            "opt_a": {
                "name": opt_a.name,
                "money_at_risk_usd": _safe_int(getattr(opt_a, "money_at_risk_usd", 1000), 1000),
                "time_required_hours_per_week": _safe_int(
                    getattr(opt_a, "time_required_hours_per_week", 10), 10
                ),
                "stress_fit": getattr(opt_a.stress_fit, "value", "Medium"),
                "relationships_impact": getattr(opt_a.relationships_impact, "value", "Medium"),
                "summary": getattr(opt_a, "summary", "") or "",
                "criteria": _criteria_safe(getattr(opt_a, "criteria", {}) or {}),
            },
            "opt_b": {
                "name": opt_b.name,
                "money_at_risk_usd": _safe_int(getattr(opt_b, "money_at_risk_usd", 1000), 1000),
                "time_required_hours_per_week": _safe_int(
                    getattr(opt_b, "time_required_hours_per_week", 10), 10
                ),
                "stress_fit": getattr(opt_b.stress_fit, "value", "Medium"),
                "relationships_impact": getattr(opt_b.relationships_impact, "value", "Medium"),
                "summary": getattr(opt_b, "summary", "") or "",
                "criteria": _criteria_safe(getattr(opt_b, "criteria", {}) or {}),
            },
        },
    }


def apply_snapshot(snapshot: dict) -> None:
    """
    Load a snapshot into session state (in-place).
    Safe defaults: missing fields won't crash.

    Accepts:
    - current format: {"decision": {...}, "options": {...}}
    - mildly older/flattened formats (best effort)
    """
    if not isinstance(snapshot, dict):
        raise ValueError("Snapshot must be a JSON object (dict).")

    d = get_decision()
    opt_a, opt_b = get_options()

    # Current format
    dec = snapshot.get("decision") if isinstance(snapshot.get("decision"), dict) else {}
    opts = snapshot.get("options") if isinstance(snapshot.get("options"), dict) else {}

    # Back-compat (if you ever change your shape)
    if not dec and ("title" in snapshot or "category" in snapshot):
        dec = {
            "title": snapshot.get("title", ""),
            "category": snapshot.get("category", ""),
            "limits": snapshot.get("limits", {}),
        }
    if not opts and ("opt_a" in snapshot or "opt_b" in snapshot):
        opts = {"opt_a": snapshot.get("opt_a", {}), "opt_b": snapshot.get("opt_b", {})}

    d.title = (dec.get("title") or "").strip()
    d.category = (dec.get("category") or "").strip()

    lim = dec.get("limits") if isinstance(dec.get("limits"), dict) else {}
    d.limits.money_max_usd = _safe_int(lim.get("money_max_usd", 1000), 1000)
    d.limits.time_hours_per_week = _safe_int(lim.get("time_hours_per_week", 10), 10)
    d.limits.stress = _risk_from_value(lim.get("stress"))
    d.limits.relationships = _risk_from_value(lim.get("relationships"))
    d.limits.confirmed = bool(lim.get("confirmed", False))

    a = opts.get("opt_a") if isinstance(opts.get("opt_a"), dict) else {}
    opt_a.name = (a.get("name") or "Option A").strip() or "Option A"
    opt_a.money_at_risk_usd = _safe_int(a.get("money_at_risk_usd", 1000), 1000)
    opt_a.time_required_hours_per_week = _safe_int(a.get("time_required_hours_per_week", 10), 10)
    opt_a.stress_fit = _risk_from_value(a.get("stress_fit"))
    opt_a.relationships_impact = _risk_from_value(a.get("relationships_impact"))
    opt_a.summary = a.get("summary", "") or ""
    opt_a.criteria = dict(a.get("criteria", {}) or {})

    b = opts.get("opt_b") if isinstance(opts.get("opt_b"), dict) else {}
    opt_b.name = (b.get("name") or "Option B").strip() or "Option B"
    opt_b.money_at_risk_usd = _safe_int(b.get("money_at_risk_usd", 1000), 1000)
    opt_b.time_required_hours_per_week = _safe_int(b.get("time_required_hours_per_week", 10), 10)
    opt_b.stress_fit = _risk_from_value(b.get("stress_fit"))
    opt_b.relationships_impact = _risk_from_value(b.get("relationships_impact"))
    opt_b.summary = b.get("summary", "") or ""
    opt_b.criteria = dict(b.get("criteria", {}) or {})


# -----------------------------
# Past Decisions (disk storage)
# -----------------------------
def _slug(s: str, *, max_len: int = 40) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return (s[:max_len] or "decision").strip("-") or "decision"


def save_current_snapshot(label: str | None = None) -> str:
    """
    Saves current snapshot to disk and returns file_id (filename).
    """
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

    snap = snapshot_current()
    title = ((snap.get("decision") or {}).get("title") or "").strip()
    base = _slug(label or title or "decision")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_id = f"{ts}__{base}.json"
    path = SAVE_DIR / file_id

    path.write_text(json.dumps(snap, indent=2, ensure_ascii=False), encoding="utf-8")
    return file_id


def list_saved_snapshots() -> list[dict[str, Any]]:
    """
    Returns newest-first list of saved decisions with basic metadata.
    """
    if not SAVE_DIR.exists():
        return []

    items: list[dict[str, Any]] = []
    for p in sorted(SAVE_DIR.glob("*.json"), key=lambda x: x.name, reverse=True):
        try:
            raw = p.read_text(encoding="utf-8")
            snap = json.loads(raw) if raw else {}
            dec = snap.get("decision", {}) if isinstance(snap.get("decision"), dict) else {}
            title = str(dec.get("title", "")).strip() or "Untitled"
            category = str(dec.get("category", "")).strip()
            saved_at = str(snap.get("saved_at", "")).strip() or p.name.split("__")[0]

            items.append(
                {
                    "file_id": p.name,
                    "title": title,
                    "category": category,
                    "saved_at": saved_at,
                    "path": str(p),
                }
            )
        except Exception:
            # Corrupt file? Skip it (don’t brick Past Decisions screen).
            continue

    return items


def load_snapshot_by_id(file_id: str) -> dict:
    path = SAVE_DIR / file_id
    if not path.exists():
        raise FileNotFoundError(f"Snapshot not found: {file_id}")
    snap = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(snap, dict):
        raise ValueError("Snapshot file did not contain a JSON object.")
    return snap


def delete_snapshot(file_id: str) -> None:
    path = SAVE_DIR / file_id
    if path.exists():
        path.unlink()


# -----------------------------
# Existing UI helper
# -----------------------------
def risk_radio(
    label: str,
    key: str,
    default: Risk | None,
    *,
    label_visibility: str = "visible",
) -> Risk:
    labels = ["Low", "Medium", "High"]
    mapping = {"Low": Risk.LOW, "Medium": Risk.MEDIUM, "High": Risk.HIGH}
    inv = {v: k for k, v in mapping.items()}

    default_label = inv.get(default, "Medium") if default is not None else "Medium"
    idx = labels.index(default_label)

    choice = st.radio(
        label,
        labels,
        index=idx,
        key=key,
        horizontal=True,
        label_visibility=label_visibility,
    )
    return mapping[choice]
