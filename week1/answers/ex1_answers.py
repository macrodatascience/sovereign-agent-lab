"""
Exercise 1 — Answers
====================
Fill this in after running exercise1_context.py.
Run `python grade.py ex1` to check for obvious issues before submitting.
"""

# ── Part A ─────────────────────────────────────────────────────────────────

# The exact answer the model gave for each condition.
# Copy-paste from your terminal output (the → "..." part).

PART_A_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_A_XML_ANSWER      = "The Albanach"
PART_A_SANDWICH_ANSWER = "The Albanach"

# Was each answer correct? True or False.
# Correct = contains "Haymarket" or "Albanach" (both satisfy all constraints).

PART_A_PLAIN_CORRECT    = True   # True or False
PART_A_XML_CORRECT      = True
PART_A_SANDWICH_CORRECT = True

# Explain what you observed. Minimum 30 words.

PART_A_EXPLANATION = """
The model correctly identified valid venues under all three formatting styles.
Plain format selected The Haymarket Vaults (180 tokens), while XML and SANDWICH selected The Albanach (251 and 289 tokens).
This shows that formatting can subtly influence which valid option is chosen even when multiple answers satisfy constraints.
"""

# ── Part B ─────────────────────────────────────────────────────────────────

PART_B_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_B_XML_ANSWER      = "The Albanach"
PART_B_SANDWICH_ANSWER = "The Albanach"

PART_B_PLAIN_CORRECT    = True
PART_B_XML_CORRECT      = True
PART_B_SANDWICH_CORRECT = True

# Did adding near-miss distractors change any results? True or False.
PART_B_CHANGED_RESULTS = False

# Which distractor was more likely to cause a wrong answer, and why?
# Minimum 20 words.
PART_B_HARDEST_DISTRACTOR = """
The New Town Vault is the hardest distractor because it satisfies capacity (162) and availability,
but fails only on the vegan constraint, making it visually very close to a correct answer. 
"""

# ── Part C ─────────────────────────────────────────────────────────────────

# Did the exercise run Part C (small model)?
# Check outputs/ex1_results.json → "part_c_was_run"
PART_C_WAS_RUN = True   # True or False

PART_C_PLAIN_ANSWER    = "Haymarket Vaults"
PART_C_XML_ANSWER      = "The Haymarket Vaults"
PART_C_SANDWICH_ANSWER = "The Haymarket Vaults"

# Explain what Part C showed, or why it wasn't needed. Minimum 30 words.
PART_C_EXPLANATION = """
Part C showed that testing with a smaller model (Gemma 2 2B) still correctly solved the task under all formats.
All three prompting styles converged on Haymarket Vaults despite increased model weakness along with the distractors in the dataset. 
Surprisingly no major degradation in reasoning was observed across all formats. This suggests the dataset was not sufficiently 
adversarial to expose structural weaknesses, and both plain and structured prompting remained effective.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """ 

Context formatting matters most when multiple valid or near-valid options exist, because LLMs do not strictly execute rules but instead distribute attention across tokens and patterns. 
Structured formats like XML or sandwich prompting improve reliability by explicitly segmenting information and reinforcing constraints, reducing the chance that distractors or positional bias 
influence the output. This effectively raises the SNR ratio in the context window, making it easier for the model to consistently apply all constraints rather than over-weighting partial matches. 
The effect becomes most visible when datasets contain competing candidates that partially satisfy requirements, where small differences in formatting can change which option the model selects.

"""
