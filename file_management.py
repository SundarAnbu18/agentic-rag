from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import subprocess
load_dotenv()

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

def terminal_command(command: str) -> str:
    """Execute a terminal command and return the output."""
    return subprocess.run(command, shell=True, capture_output=True, text=True).stdout

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[terminal_command],
    system_prompt="You are a helpful assistant that can execute terminal commands.",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "remove the text sundar from documentation.txt"}]}
)

print(result["messages"][-1].content_blocks)