import json
from pathlib import Path


def load_seen(path: str) -> set[str]:
    p = Path(path)
    if not p.exists():
        return set()
    data = json.loads(p.read_text())
    return set(data)


def save_seen(path: str, ids: set[str]) -> None:
    p = Path(path)
    p.write_text(json.dumps(sorted(ids), indent=2) + "\n")
