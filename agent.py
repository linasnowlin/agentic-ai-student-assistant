import ast
import json
import math
import operator
from typing import Callable


# ============================================================
# 1. SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """You are a helpful Student Assistant Agent.

Your job is to understand the user's request and decide whether a tool is needed.

Use the calculator tool for arithmetic questions.

Use the student_information tool when the user asks about a student's
department or student details.

Use the attendance tool when the user asks about a student's attendance.

For general questions such as "What is Python?", answer normally using
your language model knowledge. Do not use student tools unnecessarily.

If a student is not found in the student database, clearly say that
the student was not found. Do not guess student information.

After using a tool, use the tool result to provide a clear final answer.
"""


# Maximum number of tool-calling rounds
MAX_TOOL_ROUNDS = 5


# ============================================================
# 2. STUDENT DATABASE
# ============================================================

STUDENTS = {
    "Arun": {
        "department": "CSE",
        "attendance": 82
    },

    "Priya": {
        "department": "AI",
        "attendance": 91
    }
}


# ============================================================
# 3. TOOLS AVAILABLE TO THE LLM
# ============================================================

TOOLS = [

    # --------------------------------------------------------
    # Calculator Tool
    # --------------------------------------------------------

    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a basic arithmetic expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": (
                            "Arithmetic using numbers, parentheses, "
                            "+, -, *, /, //, %, and **."
                        ),
                    }
                },
                "required": ["expression"],
                "additionalProperties": False,
            },
        },
    },


    # --------------------------------------------------------
    # Student Information Tool
    # --------------------------------------------------------

    {
        "type": "function",
        "function": {
            "name": "student_information",
            "description": (
                "Get information about a student, "
                "including their department."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the student.",
                    }
                },
                "required": ["name"],
                "additionalProperties": False,
            },
        },
    },


    # --------------------------------------------------------
    # Attendance Tool
    # --------------------------------------------------------

    {
        "type": "function",
        "function": {
            "name": "attendance",
            "description": "Get the attendance percentage of a student.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the student.",
                    }
                },
                "required": ["name"],
                "additionalProperties": False,
            },
        },
    },
]


# ============================================================
# 4. CALCULATOR OPERATORS
# ============================================================

_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


# ============================================================
# 5. CALCULATOR FUNCTION
# ============================================================

def calculate(expression: str) -> int | float:
    """
    Safely evaluate a basic arithmetic expression.
    """

    if len(expression) > 200:
        raise ValueError("Expression is too long.")

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        raise ValueError("Invalid arithmetic expression.")

    # Prevent overly complicated expressions
    if sum(1 for _ in ast.walk(tree)) > 64:
        raise ValueError("Expression is too complex.")

    def evaluate(node: ast.AST) -> int | float:

        # Numbers
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):

            return node.value


        # Positive / negative numbers
        if isinstance(node, ast.UnaryOp):

            if type(node.op) in _UNARY_OPERATORS:

                return _UNARY_OPERATORS[type(node.op)](
                    evaluate(node.operand)
                )


        # Binary operations
        if isinstance(node, ast.BinOp):

            if type(node.op) in _BINARY_OPERATORS:

                left = evaluate(node.left)
                right = evaluate(node.right)


                # Limit exponent
                if isinstance(node.op, ast.Pow) and abs(right) > 100:

                    raise ValueError(
                        "Exponent must be between -100 and 100."
                    )


                try:

                    result = _BINARY_OPERATORS[type(node.op)](
                        left,
                        right
                    )

                except ZeroDivisionError:

                    raise ValueError("Cannot divide by zero.")


                # Check result
                if isinstance(result, float) and not math.isfinite(result):

                    raise ValueError(
                        "Result is outside the supported numeric range."
                    )


                return result


        raise ValueError(
            "Only basic arithmetic operations are allowed."
        )


    return evaluate(tree.body)


# ============================================================
# 6. STUDENT INFORMATION FUNCTION
# ============================================================

def student_information(name: str) -> str:
    """
    Return the department of a student.
    """

    # Make the search case-insensitive
    student_name = name.strip().lower()

    for stored_name, student in STUDENTS.items():

        if stored_name.lower() == student_name:

            return (
                f"{stored_name} is from "
                f"{student['department']} department."
            )


    # Student not found
    return (
        f"{name} was not found in the student database."
    )


# ============================================================
# 7. ATTENDANCE FUNCTION
# ============================================================

def attendance(name: str) -> str:
    """
    Return the attendance percentage of a student.
    """

    # Make the search case-insensitive
    student_name = name.strip().lower()

    for stored_name, student in STUDENTS.items():

        if stored_name.lower() == student_name:

            return (
                f"{stored_name}'s attendance is "
                f"{student['attendance']}%."
            )


    # Student not found
    return (
        f"{name} was not found in the student database."
    )


# ============================================================
# 8. TOOL EXECUTION FUNCTION
# ============================================================

def execute_tool(name: str, arguments: dict) -> str:
    """
    Execute the tool selected by the LLM.
    """

    # Calculator
    if name == "calculate":

        return str(
            calculate(arguments["expression"])
        )


    # Student information
    if name == "student_information":

        return student_information(
            arguments["name"]
        )


    # Attendance
    if name == "attendance":

        return attendance(
            arguments["name"]
        )


    # Unknown tool
    return f"Unknown tool: {name}"


# ============================================================
# 9. MAIN AGENT FUNCTION
# ============================================================

def run_agent(
    client,
    model: str,
    messages: list[dict[str, str]],
    on_tool: Callable[[str, dict, str], None] | None = None,
) -> str:
    """
    Run the Agentic AI system.

    The LLM decides whether a tool is needed and
    which tool should be used.
    """

    # Create conversation for the LLM
    conversation = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        *messages[-20:],
    ]


    # Allow multiple tool calls if necessary
    for _ in range(MAX_TOOL_ROUNDS):

        # Ask the LLM
        response = client.chat.completions.create(

            model=model,

            messages=conversation,

            tools=TOOLS,

            # The LLM automatically decides
            # whether a tool is needed
            tool_choice="auto",

            temperature=0.2,
        )


        # Get the assistant message
        assistant_message = response.choices[0].message


        # ----------------------------------------------------
        # If no tool is needed
        # ----------------------------------------------------

        if not assistant_message.tool_calls:

            return (
                assistant_message.content
                or "I couldn't generate a response."
            )


        # ----------------------------------------------------
        # Add assistant's tool request to conversation
        # ----------------------------------------------------

        conversation.append(
            assistant_message.model_dump(
                exclude_none=True
            )
        )


        # ----------------------------------------------------
        # Execute each requested tool
        # ----------------------------------------------------

        for tool_call in assistant_message.tool_calls:

            name = tool_call.function.name

            arguments = {}


            try:

                # Convert JSON arguments into Python dictionary
                arguments = json.loads(
                    tool_call.function.arguments or "{}"
                )


                # Execute selected tool
                result = execute_tool(
                    name,
                    arguments
                )


            except (
                ArithmeticError,
                KeyError,
                TypeError,
                ValueError,
                json.JSONDecodeError,
            ) as error:

                result = f"Tool error: {error}"


            # Show tool usage in main.py
            if on_tool:

                on_tool(
                    name,
                    arguments,
                    result
                )


            # Send tool result back to the LLM
            conversation.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )


    # Tool-call limit reached
    return (
        "I reached the tool-call limit before finishing. "
        "Please try a simpler request."
    )