"""Tools the agent is allowed to run, plus the JSON Schema descriptions the
LLM reads when choosing a tool."""
import ast
import operator
from config import LEAVE_BALANCE


def get_leave_balance(employee_id: str) -> str:
    """Look up the remaining leave days for one employee code."""
    balance = LEAVE_BALANCE.get(employee_id.strip().upper())
    return str(balance) if balance is not None else f"Unknown employee code: {employee_id}"


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
    """Evaluate a basic arithmetic expression such as (12 + 8) - 5."""
    try:
        return str(_evaluate(ast.parse(expression, mode="eval").body))
    except Exception as error:
        return f"Calculator error: {error}"


TOOL_FUNCTIONS = {"get_leave_balance": get_leave_balance, "calculator": calculator}

# These descriptions are what the LLM reads when deciding which tool to call
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_leave_balance",
            "description": "Get the remaining leave days for a single employee code, for example EMP101.",
            "parameters": {
                "type": "object",
                "properties": {"employee_id": {"type": "string"}},
                "required": ["employee_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate an arithmetic expression using + - * / and brackets.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
]

if __name__ == "__main__":
    print("get_leave_balance('EMP101') ->", get_leave_balance("EMP101"))
    print("calculator('12 + 8') ->", calculator("12 + 8"))
    print("calculator('15 - 12') ->", calculator("15 - 12"))