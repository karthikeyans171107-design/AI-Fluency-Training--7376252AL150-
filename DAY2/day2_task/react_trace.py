"""Day 2, Part D: print the agent's real ReAct trace to compare with your paper trace."""
from agent import agent

QUESTION = ("Which is cheaper: a laptop and a mouse with a 10% student discount, "
            "or a laptop, a mouse and a keyboard with a 20% bundle discount? By how much?")

print("QUESTION:", QUESTION, "\n")
print("--- the agent's actions and observations ---")
answer = agent(QUESTION, max_steps=8)
print("\nFINAL ANSWER:", answer)