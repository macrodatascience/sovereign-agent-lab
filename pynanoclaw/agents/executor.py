from sovereign_agent.agents.research_agent import run_research_agent


def execute_task(task: str, max_turns: int = 8) -> dict:
    """
    PyNanoClaw executor wrapper around the existing LangGraph research agent.
    """
    return run_research_agent(task, max_turns=max_turns)