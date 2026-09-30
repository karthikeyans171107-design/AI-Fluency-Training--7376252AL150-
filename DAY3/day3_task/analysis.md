# Analysis: LLMs, Tools and Agents on a Student Attendance Scenario

**Scenario:** A college keeps attendance percentages in a private register
(BA0001: 82, BA0002: 68, BA0003: 91). One tool, `get_attendance(roll_no)`,
looks up a student's percentage. I ran the same questions with and without it.

## 3.1 Concepts

A Large Language Model (LLM) predicts the next words from patterns in its
training text. It answers general questions well, such as explaining
attendance rules or writing a reminder, but it guesses when the answer is
private data it never saw, like BA0002's real attendance.

An agent is an LLM that can act instead of only replying. A chat reply is
one text answer from memory. An agent can decide it needs outside
information, call a function, read the result and then answer.

A tool is a normal function the model may request. Its schema (name,
description, parameters) is all the model knows about it, since it cannot see
the code. The description tells the model when the tool applies, and the
parameters tell it what to send.

Flow of one call: the user asks "What is BA0002's attendance?"; the model
sees the tool schema and replies with a call to `get_attendance("BA0002")`;
my program runs the function and gets "BA0002: 68%"; the result goes back to
the model as a tool message; the model writes the final answer, "68%".

A tool should return plain text, even on failure, because an exception would
crash the program. A message like "Error: no student BA0999 found" goes back
to the model, which can explain the problem to the user.

## 3.2 Comparison Table

| Basis | Plain LLM | LLM with one tool |
|---|---|---|
| Source of the answer | Training memory | Live result from the register |
| Fetch or compute outside memory? | No | Yes, via the function |
| Reliability on factual/numeric questions | Low, may guess confidently | High, value comes from the data |
| Transparency | Only the final text | Tool call and result are visible |
| Speed / cost | One call, cheaper | At least two calls, slower |

## 3.3 Implementation

`tools.py` holds the tool and its schema. `plain_llm.py` asks the questions
with no tools. `tool_llm.py` asks the same questions with the tool attached.
Screenshots of both runs are in `screenshots/`.

## 3.4 Observation

1. *What is BA0002's attendance percentage?* (needs the tool)
   Plain LLM: it said it had no access to the college's attendance register
   and could not know the value, and asked me to check the register. Answer
   given: none, so it refused. With the tool: the model called
   `get_attendance("BA0002")`, received "BA0002: 68%", and answered 68%. This
   is correct, and the tool result was used in the final answer.

2. *Who has higher attendance, BA0001 or BA0003, and by how many points?*
   (needs the tool)
   Plain LLM: it did not have the data, so it either asked for the figures or
   guessed a confident-sounding number. Its answer was not reliable and
   could not be checked. With the tool: the model called the function for
   both roll numbers (82 and 91) and answered that BA0003 is higher by 9
   points. This is correct.

3. *Write a two-line reminder telling students to attend regularly.*
   (no tool needed)
   Plain LLM: it answered well straight away, because this is ordinary
   writing that needs no private data. With the tool available: the model
   answered directly with no tool call, which shows that having a tool does
   not force the model to use it when it is not needed.

Overall, the plain LLM was reliable only on the writing task. On the two
attendance questions it refused or guessed. The tool-enabled run answered
both correctly by calling the tool with the right arguments and using the
returned values.

## 3.5 Suitability and Conclusion

The plain prompt was enough for the reminder, because the answer is
generated text and needs no lookup. A tool was necessary for every question
about actual attendance, because the data is private and any number the model
produced alone would be invented.

In general, a plain LLM is sufficient for explaining, writing, summarising
and reasoning over information already in the prompt. A problem needs a tool
when the answer depends on private, current or exact data that the model
cannot reliably produce from memory. If a wrong answer would be a fabricated
fact and not just poor wording, the model needs a tool. The tool also makes
the answer traceable, since the call shows where the number came from.