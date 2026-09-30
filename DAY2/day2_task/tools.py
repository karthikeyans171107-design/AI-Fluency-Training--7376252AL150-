import ast
import operator

# The shop's prices: the fact the model cannot know, so it must look it up with a tool.
PRICES = {
    "LAPTOP": 52000,
    "MOUSE": 800,
    "KEYBOARD": 1500,
}


def get_price(item: str) -> str:
    """Look up the price of one shop item."""
    price = PRICES.get(item.strip().upper())
    return str(price) if price is not None else f"Unknown item: {item}"


# A safe calculator: only numbers and + - * / ( ) are allowed. Never use eval().
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.USub: operator.neg}


def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.operand))
    raise ValueError("Unsupported expression")


def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression such as (52000 + 800) * 0.9."""
    try:
        return str(_evaluate(ast.parse(expression, mode="eval").body))
    except Exception as error:
        return f"Calculator error: {error}"


TOOL_FUNCTIONS = {"get_price": get_price, "calculator": calculator}

# These descriptions are what the LLM reads when deciding which tool to call
TOOLS = [
    {"type": "function", "function": {
        "name": "get_price",
        "description": "Get the shop price of a single item: LAPTOP, MOUSE or KEYBOARD.",
        "parameters": {"type": "object",
                       "properties": {"item": {"type": "string"}},
                       "required": ["item"]}}},
    {"type": "function", "function": {
        "name": "calculator",
        "description": "Evaluate an arithmetic expression using + - * / and brackets.",
        "parameters": {"type": "object",
                       "properties": {"expression": {"type": "string"}},
                       "required": ["expression"]}}},
]

if __name__ == "__main__":
    print("get_price('laptop') ->", get_price("laptop"))
    print("calculator('(52000 + 800) * 0.9') ->", calculator("(52000 + 800) * 0.9"))