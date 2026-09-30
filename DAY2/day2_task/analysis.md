# Direct Prompting vs Chain-of-Thought vs ReAct

**Scenario.** A college fee assistant. The course fees are facts the model cannot know: CS101 = Rs. 12,000, AI202 = Rs. 18,000, DS303 = Rs. 15,000. Two kinds of question are used. Reasoning-only questions give every number (e.g. three fees, a 15% scholarship, 4 instalments, correct answer Rs. 9,562.50). The tool question gives no fees: *"Which is cheaper: CS101 and AI202 with a 10% scholarship, or all three courses with a 25% scholarship? By how much?"* Correct answer: Rs. 27,000 vs Rs. 33,750, so the first is cheaper by Rs. 6,750.

## 3.1 Explanation of each approach

**Direct prompting** sends the question and asks for only the final answer. It uses no tools and shows no reasoning, so the answer comes straight from the model's own knowledge. It is fine for simple, well-known facts but fails when several dependent steps must be squeezed into one guess, or when a needed fact is missing. In my scenario the model had to apply the scholarship and divide into instalments in one go, and on the fee comparison it could not know the fees. On the instalment question a direct answer is likely to skip a step such as the scholarship and give a wrong amount, and on the fee comparison it could not give a reliable answer because it had no way to find the fees: it either guessed or asked for them.

**Chain-of-Thought (CoT)** asks the model to solve the problem step by step, showing each calculation, and to end with "Final Answer:". It uses no tools. Writing each step down makes multi-step arithmetic and logic much more reliable, but CoT still cannot fetch facts it does not have: it can reason neatly about invented fees and still be wrong. On the instalment question CoT worked out the total of Rs. 45,000, the 15% scholarship of Rs. 6,750, the payable Rs. 38,250 and the instalment of Rs. 9,562.50, with every step visible and checkable. On the fee comparison it had the same limitation as direct prompting: without the fees it could not reach a trustworthy answer, however tidy its steps were.

**ReAct** interleaves Thought, Action and Observation. The model is given two tools, `get_course_fee` and `calculator`, and decides for itself when to call one. Each tool result is sent back as an observation, and the loop repeats until the model answers without asking for a tool (or a step limit is reached). On the fee comparison it looked up the three fees, used the calculator for both totals and the difference, and answered Rs. 6,750 cheaper for CS101 + AI202. Its limit showed when it first asked which course was "the third": it is only as capable as its tools and instructions, and it needs several model calls. This matched my run: the trace showed the three lookups, the calculator steps and the final answer.

## 3.2 Comparison table

| Basis | Direct prompting | Chain-of-Thought | ReAct agent |
|---|---|---|---|
| Reasoning depth | None visible | Step by step | Step by step, plus deciding what to look up |
| Tool usage | None | None | `get_course_fee`, `calculator` |
| Reliability on multi-step questions | Low, steps get skipped | Good if all facts are given | Highest, facts and arithmetic come from tools |
| Transparency | Only the final answer | Full written reasoning | Full trace of thoughts, actions, observations |
| Speed / cost | Fastest, cheapest | Longer output, more tokens | Slowest, several calls |
| Consistency across runs | Varies on multi-step questions | Mostly consistent, can vary above temperature 0 | Consistent, tool results are fixed |

## 3.3 Self-consistency observation

I ran the CoT instalment question five times at temperature 0.8. All five answers were Rs. 9,562.50, so the majority answer was correct (true value Rs. 9,562.50). At temperature 0 the five runs were again identical. This shows the model handles this question reliably, so the randomness at 0.8 did not change the outcome here. A non-zero temperature lets the model take different reasoning paths, so majority voting filters out one-off mistakes. At temperature 0 the runs repeat each other, which gives consistency but not correctness: if the best path has an error, every run repeats it.

## 3.4 Suitability analysis

ReAct is the most suitable approach for this scenario. The fee comparison depends on facts the model cannot know, and neither direct prompting nor CoT has a tool to get them; the table shows they can only guess. Self-consistency does not fix this either, since even five identical answers would rest on invented numbers. ReAct fetches the fees, does exact arithmetic with the calculator, and leaves a trace that can be checked. Its extra cost in time and calls is worth it when a wrong fee matters.

## 3.5 Conclusion

Use direct prompting for simple, well-known questions where speed and cost matter and an error is cheap. Use Chain-of-Thought (with self-consistency if it matters) when the problem needs several reasoning steps but everything required is already in the prompt or the model's knowledge, such as arithmetic, counting and logic. Use a ReAct agent when the answer depends on information the model lacks or that changes, such as fees, prices or records, or when the process must be inspectable. Choose the cheapest approach that can actually get every fact it needs.