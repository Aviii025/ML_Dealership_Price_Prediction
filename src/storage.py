"""Persist submitted vehicle evaluations to CSV files (one per vehicle type).

Note: on Streamlit Community Cloud the filesystem is ephemeral, so these files
are wiped whenever the app reboots or is redeployed. Use the download button
on each page to export them.
"""

from __future__ import annotations

import threading
from datetime import datetime
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "submissions"

# Columns that look numeric but must keep "+" prefixes and leading zeros.
TEXT_COLUMNS = {"seller_phone": str, "registration_number": str}

# All sessions share one process, so serialise read-modify-write cycles.
_LOCK = threading.Lock()


def _csv_path(vehicle_type: str) -> Path:
    return DATA_DIR / f"{vehicle_type}s.csv"


def _read(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=TEXT_COLUMNS)


def save_submission(vehicle_type: str, record: dict) -> Path:
    """Append one submission to the vehicle type's CSV and return its path."""
    path = _csv_path(vehicle_type)
    row = {"submitted_at": datetime.now().isoformat(timespec="seconds"), **record}
    with _LOCK:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame([row])
        if path.exists():
            df = pd.concat([_read(path), df], ignore_index=True)
        df.to_csv(path, index=False)
    return path


def load_submissions(vehicle_type: str) -> pd.DataFrame:
    """Load all saved submissions for a vehicle type (empty if none)."""
    path = _csv_path(vehicle_type)
    with _LOCK:
        if not path.exists():
            return pd.DataFrame()
        return _read(path)
