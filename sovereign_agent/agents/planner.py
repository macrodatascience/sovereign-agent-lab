from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv
import re

load_dotenv()

llm = ChatOpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.getenv("NEBIUS_KEY"),
    model=os.getenv("RESEARCH_MODEL", "Qwen/Qwen3-32B"),
    temperature=0,
)

SYSTEM_PROMPT = """
You are a STRICT execution planner for an autonomous tool-using agent.

You convert tasks into atomic tool-executable steps.

RULES:
- Output ONLY numbered steps
- No explanations, no markdown, no commentary
- Each step MUST correspond to ONE tool action or ONE deterministic transformation
- NEVER describe abstract reasoning steps (like "analyze", "extract", "understand")
- For Edinburgh pub tasks, only suggest known venues: The Albanach, The Haymarket Vaults, The Guilford Arms, The Bow Bar

TOOL-FIRST PLANNING RULES:

If searching:
- Step must call search_web

If evaluating candidates:
- Step must explicitly list each candidate evaluation separately

If information must be structured:
- You MUST assume a parser function will handle extraction

DO NOT:
- Do not write “extract list”
- Do not write “analyze results”
- Do not group multiple actions in one step

GOOD EXAMPLES:
1. search_web for venues in Edinburgh with capacity ≥160
2. check_pub_availability for The Albanach
3. check_pub_availability for The Haymarket Vaults

BAD EXAMPLES:
- Extract list of venues
- Analyze search results
- Evaluate all venues together

FORMAT:
1. ...
2. ...
3. ...
"""

def plan_task(task: str) -> list[str]:
    response = llm.invoke([
        HumanMessage(content=f"{SYSTEM_PROMPT}\n\nTask: {task}")
    ])

    text = response.content.strip()

    steps = []

    for line in text.splitlines():
        match = re.match(r"^\d+\.\s+(.+)$", line.strip())
        if match:
            steps.append(match.group(1).strip())

    if not steps:
        raise ValueError(f"Planner produced invalid output:\n\n{text}")


    deduped = []
    seen = set()

    for step in steps:
        normalized = step.lower().strip().rstrip(".")
        if normalized not in seen:
            deduped.append(step)
            seen.add(normalized)

    return deduped[:4]