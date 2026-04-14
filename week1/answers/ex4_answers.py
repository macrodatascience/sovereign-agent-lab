"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ['search_venues', 'get_venue_details']

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = "No venue that meet the 300 people capacity was found"

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True   # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
After changing The Albanach's status from 'available' to 'full', it was excluded from the search results during the MCP tool query. In the baseline run, both The Albanach and The Haymarket Vaults were returned as valid venue options. After the modification, only The Haymarket Vaults remained in the result set for Query 1. No changes were required in the LangGraph client, tool interface, or agent logic files. Only the backend MCP server data file (mcp_venue_server.py) was modified, confirming that system behavior changed solely due to external data state.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 302   # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 291   # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP provides a standard protocol for tool discovery, execution, and schema validation, rather than just separating tools into another file. 
The agent can dynamically discover available tools at runtime, validate arguments through a structured interface, and invoke external services without hardcoding tool imports or function signatures. This makes tools reusable across different agents and allows backend changes (like venue availability or tool logic) to immediately affect behavior without modifying the LangGraph code. 
It also enforces a clean boundary between reasoning (agent) and execution (tool server), improving modularity, scalability, and interoperability.
"""

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────
#
# (The variable below is still called WEEK_5_ARCHITECTURE because the
# grader reads that exact name. Don't rename it — but read the updated
# prompt: the question is now about PyNanoClaw, the hybrid system the
# final assignment will have you build.)
#
# This is a forward-looking, speculative question. You have NOT yet seen
# the material that covers the planner/executor split, memory, or the
# handoff bridge in detail — that is what the final assignment (releases
# 2026-04-18) is for. The point of asking it here is to check that you
# have read PROGRESS.md and can imagine how the Week 1 pieces grow into
# PyNanoClaw.
#
# Read PROGRESS.md in the repo root. Then write at least 5 bullet points
# describing PyNanoClaw as you imagine it at final-assignment scale.
#
# Each bullet should:
#   - Name a component (e.g. "Planner", "Memory store", "Handoff bridge",
#     "Rasa MCP gateway")
#   - Say in one clause what that component does and which half of
#     PyNanoClaw it lives in (the autonomous loop, the structured agent,
#     or the shared layer between them)
#
# You are not being graded on getting the "right" architecture — there
# isn't one right answer. You are being graded on whether your description
# is coherent and whether you have thought about which Week 1 file becomes
# which PyNanoClaw component.
#
# Example of the level of detail we want:
#   - The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
#     Qwen3-Next-Thinking) that takes the raw task and produces an ordered
#     list of subgoals. It lives upstream of the ReAct loop in the
#     autonomous-loop half of PyNanoClaw, so the Executor never sees an
#     ambiguous task.

WEEK_5_ARCHITECTURE = """
- Planner: This sits in the autonomous loop and decomposes the user request into structured subtasks, deciding when to search, reason, or handoff to the structured-agent half.
- Executor (LangGraph ReAct loop): This runs iterative reasoning and tool use over MCP tools like venue search, web search, and cost estimation in the autonomous loop half.
- Shared MCP Tool Server: This provides dynamically discovered tools (venue lookup, weather, booking utilities) to both LangGraph and Rasa CALM without hardcoded bindings.
- Structured Agent (Rasa CALM): This handles deterministic, auditable workflows such as booking confirmation, deposit validation, and human-facing phone-call style interactions.
- Handoff Bridge: This transfers control between autonomous loop and structured agent depending on task type (research vs. confirmation) while preserving shared state.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
In my runs, LangGraph with MCP was used for research-style tasks such as finding venues in Edinburgh. It handled tool calls dynamically, but I observed schema issues where the agent initially passed incorrect arguments before rectifying in the subsequent call. It also explored multiple venues and compared results.

Rasa CALM was used for structured booking confirmation, where it followed a strict flow: guest count, vegan requirement, and deposit validation. From my observation, it correctly escalated when the deposit exceeded £300 and rejected out-of-scope requests like parking.

Swapping them feels wrong because LangGraph is suited for exploratory, uncertain environments where tool selection and reasoning are flexible, while CALM is designed for strict, auditable business logic where deviations are not allowed. For instance, CALM enforced the deposit cut-off rule deterministically, while LangGraph struggled with enforcing such rigid constraints but excelled at discovery. This separation ensures reliability in the case of transactions and flexibility when it comes to research.
"""
