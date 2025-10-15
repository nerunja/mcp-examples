from fastmcp import FastMCP

mcp = FastMCP()

# ============ TOOLS ============

@mcp.tool()
def add(a: int, b: int) -> int:
    """ Add 2 integers a and b"""
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """ Subtract 2 integers a and b"""
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """ Multiply 2 integers a and b"""
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> float:
    """ Divide 2 integers a and b"""
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b


# ============ RESOURCES ============

@mcp.resource("greeting://hello")
def get_greeting() -> str:
    """A simple greeting resource"""
    return "Hello from MCP! This is a sample resource."

@mcp.resource("math://constants")
def get_math_constants() -> str:
    """Mathematical constants resource"""
    return """
Common Mathematical Constants:
- Ï€ (Pi): 3.14159265359
- e (Euler's number): 2.71828182846
- Ï† (Golden ratio): 1.61803398875
- âˆš2 (Square root of 2): 1.41421356237
"""


# ============ PROMPTS ============

@mcp.prompt()
def math_problem(operation: str = "+", num1: int = 5, num2: int = 3):
    """Generate a math problem prompt"""
    prompt_text = f"Solve this math problem: {num1} {operation} {num2} = ?"
    return [{"role": "user", "content": {"type": "text", "text": prompt_text}}]

@mcp.prompt()
def greeting_prompt(name: str = "World"):
    """Generate a personalized greeting prompt"""
    prompt_text = f"Create a friendly and warm greeting for {name}. Make it enthusiastic!"
    return [{"role": "user", "content": {"type": "text", "text": prompt_text}}]


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
