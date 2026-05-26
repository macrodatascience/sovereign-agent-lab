from pynanoclaw.agents.executor import execute_task
from pynanoclaw.bridge.handoff import should_handoff, handoff_to_structured
from pynanoclaw.memory.persistent_store import remember_event
from pynanoclaw.observability.tracing import start_trace, finish_trace


def run_pynanoclaw(task: str) -> dict:
    trace = start_trace(task)

    # Structured handoff path
    if should_handoff(task):
        result = handoff_to_structured(task)

        remember_event(
            "handoff",
            {
                "task": task,
                "target": result["target"],
            },
        )

        finish_trace(trace, {
            "success": True,
            "tool_calls_made": [],
            "final_answer": str(result),
        })

        return result

    # Autonomous executor path
    result = execute_task(task)

    remember_event(
        "execution",
        {
            "task": task,
            "success": result.get("success"),
        },
    )

    finish_trace(trace, result)

    return result