"""A question none of the three systems was designed for."""
from workflow import workflow
from agent import agent

QUESTION = "I need 20 days of leave in total. Which two employees, if we combine their balances, have enough leave between them?"

print("Q:", QUESTION)
print("\nWorkflow :", workflow(QUESTION))
print("\nAgent    :", agent(QUESTION))