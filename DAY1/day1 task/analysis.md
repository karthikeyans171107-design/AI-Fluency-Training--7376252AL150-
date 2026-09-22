# 3. Analysis — Employee Leave Balance Assistant

**Scenario:** A small college HR office keeps each employee's remaining
leave balance in a private record that no public LLM has ever seen
(`LEAVE_BALANCE = {"EMP101": 12, "EMP102": 8, "EMP103": 15}`). Staff ask
natural questions such as *"How many leave days does EMP102 have left?"* or
*"What is the total leave balance for EMP101 and EMP103 combined?"*

---

## 3.1 Explanation of each approach

### Plain chatbot (`chatbot.py`)
- **Data access:** None. It cannot access `LEAVE_BALANCE` at all — the
  private data is never sent to it.
- **Tools / rules:** None of either. It is a single call to the LLM with a
  generic system prompt ("You are a helpful HR assistant").
- **Handling a request start to finish:** The user's question goes straight
  to the LLM, which generates a plausible-sounding answer purely from
  language patterns it learned during training — it does not look anything
  up or verify anything.
- **Where limitations show up:** Every question that needs a real leave
  number (e.g., "How many leave days does EMP102 have left?") gets a
  guessed, usually wrong, figure, because the model has no way to know the
  actual balance. It only does well on the one question that needs no real
  data — the free-text reminder message.
- A plain chatbot mainly provides responses using an LLM alone.

### Rule-based workflow (`workflow.py`)
- **Data access:** Full, direct access to `LEAVE_BALANCE` — but only
  through hard-coded Python lookups, no LLM involved at any point.
- **Tools / rules:** Fixed `if/elif` rules plus a regular expression
  (`EMP\d{3}`) to pull employee codes out of the question text.
- **Handling a request start to finish:** The code searches the question
  for employee codes, fetches their balances from the dictionary, then
  checks the wording for keywords like "total", "combined", or "more" to
  decide which fixed branch to run, and returns a templated string.
- **Where limitations show up:** It only recognizes the exact phrasings
  its author anticipated. It answers the first three questions correctly,
  but the fourth ("Write a two-line reminder message...") contains no
  employee code, so it falls straight to "Sorry, I can only answer
  questions about employee leave balances" — it cannot generate free text
  at all.
- A rule-based workflow follows predefined steps and conditions, with no
  LLM involved.

### AI agent (`agent.py` + `tools.py`)
- **Data access:** Full access to `LEAVE_BALANCE`, but mediated — the LLM
  never sees the raw dictionary; it can only reach it by calling the
  `get_leave_balance(employee_id)` tool.
- **Tools / rules:** Two tools — `get_leave_balance` and a safe
  `calculator` — described to the model via JSON Schema, plus a system
  prompt instructing it to always use the tool instead of guessing.
- **Handling a request start to finish:** The LLM reasons about what the
  question needs, calls `get_leave_balance` for each employee code
  required, optionally calls `calculator` to total or compare the results,
  observes each tool's output, and repeats this loop until it has enough
  grounded information to produce a final natural-language answer.
- **Where limitations show up:** It is slower and more expensive than the
  other two (multiple model calls per question), and its correctness
  depends on the model reliably choosing to call the tool rather than
  answer from memory — a weak system prompt or high temperature could
  cause it to guess like the plain chatbot.
- An AI agent combines an LLM + Tools + Loop — it reasons about the task,
  selects and uses the appropriate tools, observes the results, and
  continues taking actions until the task is completed.

---

## 3.2 Comparison table

| Basis for comparison | Plain chatbot | Rule-based workflow | AI agent |
|---|---|---|---|
| Flexibility | High — answers any phrasing, but ungrounded | Very low — only exact patterns it was coded for | High — handles varied phrasing *and* stays grounded in real data |
| Decision-making | Implicit, inside the model, unverifiable | Explicit, hard-coded if/elif logic | Explicit reasoning loop — LLM chooses which tool to call at each step |
| Tool usage | None | None (direct data access, not a callable tool) | Yes — calls `get_leave_balance` and `calculator` as needed |
| Private-data access | None — model never sees real data | Full, but hard-coded and narrow | Full, but mediated and auditable through tool calls |
| Multi-step task handling | Poor — one-shot, no real reasoning over steps | Poor — each rule is a single fixed branch | Strong — loops through reason → act → observe until done |
| Automation | Fully automated, but unreliable | Fully automated, fragile to new phrasing | Fully automated, adapts to new phrasing |
| Reliability | Low for factual answers (hallucination risk) | Very high for known patterns, zero for anything else | High for factual answers (grounded via tools), minor variability in wording |

---

## 3.3 Suitability analysis

The **AI agent** is the most suitable approach for this scenario.

- **Flexibility + private-data access together:** It is the only approach
  that both understands varied natural-language phrasing (like the
  chatbot) and grounds every numeric answer in the real `LEAVE_BALANCE`
  data (like the workflow) — the chatbot has the flexibility but not the
  data access, and the workflow has the data access but not the
  flexibility.
- **Decision-making and multi-step handling:** Questions like "total leave
  balance for EMP101 and EMP103 combined" need two lookups plus an
  addition. The agent's reason → act → observe loop handles this
  naturally by calling `get_leave_balance` twice and `calculator` once;
  the workflow can only do this because a developer anticipated the exact
  word "combined," and the chatbot cannot do it reliably at all.
- **Reliability where it matters:** For factual, data-dependent questions
  the agent's answers are grounded through tool calls, unlike the
  chatbot's guesses — while still being able to answer the open-ended
  reminder-message question directly, which the rigid workflow cannot do.
- **Trade-off accepted:** The agent is slower and needs more careful
  prompt/tool design than the workflow, but for an HR assistant that must
  handle real employees asking questions in their own words, that cost is
  worth the accuracy and flexibility gained.