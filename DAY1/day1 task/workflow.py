"""System 2: a rule-based workflow. Fixed if/else rules, no LLM at all."""
import re
from config import LEAVE_BALANCE, QUESTIONS


def workflow(question):
    codes = re.findall(r"EMP\d{3}", question.upper())
    balances = [LEAVE_BALANCE[code] for code in codes if code in LEAVE_BALANCE]

    if not balances:
        return "Sorry, I can only answer questions about employee leave balances."

    text = question.lower()
    if "total" in text or "combined" in text:
        return f"Total leave balance: {sum(balances)} days"

    if "more" in text and len(codes) == 2:
        a, b = codes[0], codes[1]
        diff = LEAVE_BALANCE[a] - LEAVE_BALANCE[b]
        if diff > 0:
            return f"{a} has more leave than {b}, by {diff} days"
        elif diff < 0:
            return f"{b} has more leave than {a}, by {-diff} days"
        return f"{a} and {b} have the same leave balance"

    if len(codes) == 1:
        return f"{codes[0]} has {balances[0]} leave days left"

    return "Sorry, I do not have a rule for this type of question."


if __name__ == "__main__":
    print("\n=== SYSTEM 2: RULE-BASED WORKFLOW (no LLM) ===\n")
    for question in QUESTIONS:
        print("Q:", question)
        print("A:", workflow(question))
        print("-" * 70)