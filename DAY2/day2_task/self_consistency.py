"""Day 2, Part C: run the same CoT prompt several times and take the majority answer.

Scenario: gadget shop. QUESTIONS[0] is the instalment question
(laptop 52,000 + mouse 800 + keyboard 1,500, 10% discount, 4 instalments).
It is run at a non-zero temperature (answers can differ) and again at
temperature 0 (answers should not).
"""
import re
from collections import Counter
from config import client, MODEL, banner
from cot_compare import COT_PROMPT, QUESTIONS

RUNS = 5
TEMPERATURES = [0]          
CORRECT_ANSWER = 12217.50        


def final_answer(text):
    """Pull out the text after 'Final Answer:' (the last line of a CoT reply)."""
    for line in reversed(text.splitlines()):
        if "final answer" in line.lower():
            return line.split(":", 1)[-1].strip()
    return text.splitlines()[-1].strip() if text.strip() else "(empty)"


def normalise(answer):
    """Turn 'Rs. 12,217.50' and 'Rs. 12217.5' into the same value: 12217.50."""
    numbers = re.findall(r"\d[\d,]*(?:\.\d+)?", answer)
    if not numbers:
        return answer
    return f"{float(numbers[-1].replace(',', '')):.2f}"


def run_many(question, runs=RUNS, temperature=0.8):
    answers = []
    for attempt in range(1, runs + 1):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": COT_PROMPT},
                      {"role": "user", "content": question}],
            temperature=temperature,
        )
        answer = final_answer(response.choices[0].message.content)
        print(f"  run {attempt}: {answer}")
        answers.append(normalise(answer))
    return answers


if __name__ == "__main__":
    banner("SELF-CONSISTENCY")
    question = QUESTIONS[0]
    print("QUESTION:", question)
    for temperature in TEMPERATURES:
        print(f"\n--- temperature = {temperature} ---")
        answers = run_many(question, temperature=temperature)
        winner, count = Counter(answers).most_common(1)[0]
        correct = float(winner) == CORRECT_ANSWER if winner.replace(".", "", 1).isdigit() else False
        print(f"Majority answer ({count} of {len(answers)} runs): Rs. {winner}")
        print(f"Correct answer: Rs. {CORRECT_ANSWER:,.2f} -> majority is {'CORRECT' if correct else 'WRONG'}")