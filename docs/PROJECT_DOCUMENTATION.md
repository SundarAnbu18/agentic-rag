# Project Documentation

## Overview

This project is a compact LangChain experiment for learning agent tool-calling and local knowledge retrieval patterns. It is not a production RAG system. Instead, it provides simple building blocks that can be extended into an agentic RAG application.

The repository currently includes two runnable Python scripts:

1. `main.py` — creates an agent that can execute terminal commands.
2. `file_management.py` — creates an agent with a simple weather tool.

It also includes markdown files under `rag/` that represent local knowledge sources.

## Architecture

```text
Environment variables (.env)
        ↓
Python script
        ↓
LangChain create_agent
        ↓
LLM model via langchain-openai
        ↓
Registered Python tools
        ↓
Tool result returned to model
        ↓
Final response printed to terminal
```

## Main components

### `main.py`

Purpose: demonstrates a LangChain agent with a shell-command execution tool.

Important functions:

- `terminal_command(command: str) -> str`
  - Executes a shell command locally.
  - Returns command standard output.

- `get_weather(city: str) -> str`
  - Demo function currently not registered with the main agent.

Agent configuration:

```python
agent = create_agent(
    model="openai:gpt-5.5",
    tools=[terminal_command],
    system_prompt="You are a helpful assistant that can execute terminal commands.",
)
```

### `file_management.py`

Purpose: demonstrates a minimal custom tool.

Registered tool:

- `get_weather(city: str) -> str`

Agent configuration:

```python
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)
```

### `rag/`

Purpose: contains local markdown knowledge files.

Files:

- `hasan.md`
- `sundaranbu.md`

These files can be connected to an agent by defining reader tools and adding them to the agent's `tools` list.

## Setup guide

1. Install uv if needed:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Install project dependencies:

   ```bash
   uv sync
   ```

3. Create `.env`:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. Run the main script:

   ```bash
   uv run main.py
   ```

## Extending the project into agentic RAG

Add file-reading tools:

```python
from pathlib import Path


def read_hasan_profile() -> str:
    """Read the C P Hasan knowledge file."""
    return Path("rag/hasan.md").read_text()


def read_sundaranbu_profile() -> str:
    """Read the Sundar Anbu knowledge file."""
    return Path("rag/sundaranbu.md").read_text()
```

Register them with the agent:

```python
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[read_hasan_profile, read_sundaranbu_profile],
    system_prompt="Answer using the local knowledge tools when relevant.",
)
```

Ask a question:

```python
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What are Hasan's frontend skills?"}]}
)
```

## Limitations

- No vector database.
- No embeddings.
- No chunking.
- No retrieval ranking.
- Markdown files are returned as complete documents.
- The terminal command tool is unsafe for public or untrusted use.

## Recommended next steps

- Replace the shell-command tool with safer, task-specific tools.
- Add RAG file reader tools for `rag/*.md`.
- Add error handling around tool execution.
- Return `stderr` from failed terminal commands during development.
- Add tests for tool functions.
- Pin a model that is available for your OpenAI account.
