"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
2026-04-14 07:51:44 INFO     root  - Rasa server is up and running.
Bot loaded. Type a message and press enter (use '/stop' to exit):
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160
And how many of those guests will need vegan meals?
Your input ->  50
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  200
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Your input ->  /stop
2026-04-14 08:04:36 INFO     root  - Killing Sanic server now.
2026-04-14 08:04:36 INFO     sanic.server  - Starting worker [9397]
2026-04-14 08:04:36 INFO     sanic.server  - Stopping worker [9397]
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """

2026-04-14 07:25:44 INFO     root  - Rasa server is up and running.
Bot loaded. Type a message and press enter (use '/stop' to exit):
Your input ->  I want to book a pub for 160 people in Edinburgh with vegan options
And how many of those guests will need vegan meals?
Your input ->  160
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  500
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
Your input ->  /stop

"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "a deposit of £500 exceeds the organiser's authorised limit of £300."   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
2026-04-14 08:11:25 INFO     root  - Rasa server is up and running.
Bot loaded. Type a message and press enter (use '/stop' to exit):
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160
And how many of those guests will need vegan meals?
Your input ->  Can you arrange parking for the speakers?
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
Your input ->  /stop
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
CALM understood that the parking request is out of the booking scope and responded politely that it can only help with venue booking. 
Instead of abruptly ending the flow, it politely responded to contact the event organiser directly and also anchored back to the 
booking conversation and asked to see if it can continue with the venue booking. This clearly shows that CALM prioritised the flow and didn't
get carried away with the out of scope parking request. 
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
In the case of LangGraph we have seen that out-of-scope request simply failed and skipped execution as no relevant tools existed in the provided functions.Mean while, CALM used a LLM-driven semantic method of understanding in detecting the out-of-scope request posed to it, and responded politely redirecting those out-of-scope requests to another channel, while keeping the conversation flow and anchoring back to the with-in-scope venue booking process. This shows that CALM is more flexible than the LangGraph which is strictly following a deterministic path. 
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
I tested the cutoff guard by triggering booking requests with both valid and invalid deposit values in the Rasa chat interface. I verified that when I entered a deposit of £500, which exceeds the allowed threshold of £300, the agent correctly triggered an escalation response instead of confirming the booking. I also tested a valid deposit of £200, which allowed the booking flow to continue normally. This confirmed that the validation logic correctly enforces the business rule while preserving the conversation flow.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
In old open-source Rasa, conversation logic was driven by NLU intent classifiers, rule-based dialogue policies, and Python form validation classes. This required explicit training data and tightly defined dialogue paths, making behaviour highly predictable but expensive to maintain. In Rasa Pro CALM, the LLM dynamically handles intent understanding and slot extraction, while Python is primarily responsible for enforcing deterministic business rules such as validation constraints. This reduces engineering overhead and improves flexibility, but sacrifices strict control, reproducibility, and full predictability compared to the traditional rule-based approach.

"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """

Rasa CALM agent cannot dynamically create or modify execution paths at runtime beyond what is defined in flows.yml, and it cannot invoke tools that are not explicitly declared in the flow configuration. Its behaviour is constrained to predefined conversational and action flows, making it predictable but less flexible. LangGraph, by contrast, routes execution through a predefined graph structure using nodes and conditional edges. It can dynamically choose paths at runtime based on intermediate state, but it cannot execute logic outside the graph or use undefined tools.

In this implementation, CALM’s inability to handle requests like parking is a feature because it enforces strict adherence to the defined booking flow and prevents unsupported actions. However, from a real-world product perspective, this may be seen as a limitation in system completeness. For out-of-scope requests, LangGraph will typically fail or require an explicitly defined fallback node, whereas CALM can respond conversationally and redirect the user without requiring an explicit fallback path.

This makes CALM more structured and conversationally robust for constrained workflows, while LangGraph provides more explicit and controllable execution logic within its graph.

"""
