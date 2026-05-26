import json
from pathlib import Path
from datetime import datetime

TRACE_PATH = Path("logs/pynanoclaw_traces.jsonl")


def start_trace(task: str) -> dict:
    return {
        "task": task,
        "start_time": datetime.utcnow().isoformat(),
    }


def finish_trace(trace: dict, result: dict) -> dict:
    trace["end_time"] = datetime.utcnow().isoformat()
    trace["success"] = result.get("success", False)
    trace["tool_count"] = len(result.get("tool_calls_made", []))
    trace["final_answer"] = result.get("final_answer", "")

    TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with TRACE_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(trace) + "\n")

    return trace