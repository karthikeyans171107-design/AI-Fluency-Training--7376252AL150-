"""Day 2, Part B: the same question asked WITHOUT and WITH Chain-of-Thought.

Scenario: a small gadget shop. Questions 1-3 need only careful reasoning;
question 4 needs the shop's prices, which the model cannot know (a tool is needed).
"""
from config import client, MODEL, banner

QUESTIONS = [
    # 1. Multi-step arithmetic (all numbers are in the question)
    "A customer buys a laptop for Rs. 52,000, a mouse for Rs. 800 and a keyboard "
    "for Rs. 1,500. She gets a 10% discount on the total and pays the rest in "
    "4 equal instalments. How much is each instalment?",
    # 2. Counting in two parts
    "The shop has 12 demo laptops. In the morning each laptop is shared by "
    "2 customers, and in the afternoon by 3 customers. How many customer demo "
    "slots happen in one day?",
    # 3. Ordering / logic
    "The laptop is pricier than the keyboard. The keyboard is pricier than the "
    "mouse. The headset is cheaper than the mouse. Which item is the most "
    "expensive and which is the cheapest?",
    # 4. Needs external information (the shop's prices) -> only ReAct can answer it
    "Which is cheaper: a laptop and a mouse with a 10% student discount, or a "
    "laptop, a mouse and a keyboard with a 20% bundle discount? By how much?",
]

DIRECT_PROMPT = "You are a helpful assistant. Give only the final answer. Do not explain."

COT_PROMPT = ("You are a helpful assistant. Solve the problem step by step. "
              "Number each step and show the calculation in that step. "
              "After the steps, write the last line exactly as: Final Answer: <answer>")


def ask(system_prompt, question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": question}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    banner("CHAIN-OF-THOUGHT COMPARISON")
    for number, question in enumerate(QUESTIONS, start=1):
        print("=" * 72)
        print(f"QUESTION {number}: {question}\n")
        print("--- WITHOUT CoT ---")
        print(ask(DIRECT_PROMPT, question), "\n")
        print("--- WITH CoT ---")
        print(ask(COT_PROMPT, question), "\n")