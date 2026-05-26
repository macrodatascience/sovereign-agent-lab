import json
from pathlib import Path
from datetime import datetime

MEMORY_PATH = Path("memory/pynanoclaw_memory.json")


def load_memory() -> dict:
    if not MEMORY_PATH.exists():
        return {"events": []}

    try:
        return json.loads(MEMORY_PATH.read_text())
    except json.JSONDecodeError:
        return {"events": []}


def save_memory(data: dict) -> None:
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    MEMORY_PATH.write_text(json.dumps(data, indent=2))


def remember_event(event_type: str, payload: dict) -> dict:
    memory = load_memory()

    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "payload": payload,
    }

    memory.setdefault("events", []).append(event)
    save_memory(memory)

    return event