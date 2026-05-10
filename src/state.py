import json
from datetime import date, timedelta
from pathlib import Path


def load_seen(path: str) -> dict[str, str]:
    """Load seen IDs as {id: date_string}. Migrates old list format automatically."""
    p = Path(path)
    if not p.exists():
        return {}
    data = json.loads(p.read_text())
    # Migrate from old list format to new dict format
    if isinstance(data, list):
        today = date.today().isoformat()
        return {car_id: today for car_id in data}
    return data


def save_seen(path: str, ids: dict[str, str]) -> None:
    p = Path(path)
    p.write_text(json.dumps(dict(sorted(ids.items())), indent=2) + "\n")


def cleanup_old(ids: dict[str, str], max_age_days: int = 90) -> dict[str, str]:
    """Remove entries older than max_age_days."""
    cutoff = date.today() - timedelta(days=max_age_days)
    return {
        car_id: seen_date
        for car_id, seen_date in ids.items()
        if date.fromisoformat(seen_date) >= cutoff
    }
