# src/storage.py
from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _root_dir() -> Path:
    # src/storage.py -> project root
    return Path(__file__).resolve().parents[1]


def _data_dir() -> Path:
    p = _root_dir() / "data"
    p.mkdir(parents=True, exist_ok=True)
    return p


def _db_path() -> Path:
    return _data_dir() / "decisions.jsonl"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _safe_json(obj: Any) -> Any:
    # dataclasses -> dict
    if is_dataclass(obj):
        return asdict(obj)
    return obj


def list_saved() -> list[dict[str, Any]]:
    path = _db_path()
    if not path.exists():
        return []

    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            # ignore corrupted lines rather than breaking the app
            continue

    # newest first
    out.sort(key=lambda r: r.get("saved_at", ""), reverse=True)
    return out


def save_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    """
    Appends a snapshot to data/decisions.jsonl and returns the record written.
    """
    record = {
        "id": f"dec_{int(datetime.now(timezone.utc).timestamp())}",
        "saved_at": _utc_now_iso(),
        "snapshot": snapshot,
    }

    path = _db_path()
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, default=_safe_json) + "\n")

    return record
