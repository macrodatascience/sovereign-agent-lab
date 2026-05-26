def should_handoff(task: str) -> bool:
    """
    Decide whether this task belongs to the structured agent half.
    """
    keywords = ["call", "manager", "deposit", "confirm booking", "confirmation"]

    task_lower = task.lower()

    return any(keyword in task_lower for keyword in keywords)


def handoff_to_structured(task: str) -> dict:
    """
    Stub for future Rasa/CALM handoff.
    """
    return {
        "handoff": True,
        "target": "structured_agent",
        "reason": "Task requires structured confirmation or business-rule handling.",
        "task": task,
    }