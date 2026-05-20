from google.adk.agents import Agent
from google.adk.tools import function_tool
from google.adk.runners import Runner

# Define a simple custom tool using the @function_tool decorator
@function_tool
def get_current_time() -> str:
    """Get the current UTC time."""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

@function_tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        Sum of a and b
    """
    return a + b

# Create an agent that uses these tools
my_agent = Agent(
    name="math_helper",
    model="gemini-2.5-flash",  # or "gemini-2.0-flash"
    instruction="You are a helpful math assistant. Use the tools to help users.",
    tools=[get_current_time, add_numbers],
)

# Run the agent interactively
async def main():
    runner = Runner(agent=my_agent)
    await runner.run_async(user_id="user123", message="What time is it? What is 25 + 37?")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
