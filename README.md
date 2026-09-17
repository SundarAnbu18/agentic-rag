# Agentic RAG / Tool-Calling Demo

A small Python project that demonstrates how to build a LangChain agent with tool-calling capabilities. The repository contains:

- a terminal-command agent in `main.py`,
- a simple weather-tool example in `file_management.py`, and
- markdown knowledge files in `rag/` that can be used as source material for an agentic RAG workflow.

> **Important:** `main.py` exposes a tool that can execute shell commands. Run it only in a trusted local environment and never expose it directly to untrusted users.

## Table of contents

- [Project structure](#project-structure)
- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Configuration](#configuration)
- [Running the project](#running-the-project)
- [How the code works](#how-the-code-works)
- [Knowledge files](#knowledge-files)
- [Development notes](#development-notes)
- [Security considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)

## Project structure

```text
agentic-rag/
├── README.md                 # Main project documentation
├── docs/
│   └── PROJECT_DOCUMENTATION.md
├── main.py                   # LangChain agent with terminal command tool
├── file_management.py        # Minimal LangChain tool-calling example
├── pyproject.toml            # Project metadata and dependencies
├── uv.lock                   # uv lockfile
├── .python-version           # Python version hint
├── .env                      # Local environment variables; not committed
├── .gitignore
└── rag/
    ├── hasan.md              # Knowledge profile for C P Hasan
    └── sundaranbu.md         # Knowledge profile for Sundar Anbu
```

## Features

- Uses LangChain `create_agent` to create tool-calling agents.
- Loads environment variables from `.env` using `dotenv`.
- Demonstrates how to register Python functions as tools.
- Includes local markdown knowledge files for RAG-style experiments.
- Uses `uv` for dependency management.

## Requirements

- Python `>=3.14` as configured in `pyproject.toml`
- [`uv`](https://github.com/astral-sh/uv)
- An OpenAI API key compatible with `langchain-openai`

## Setup

Install dependencies:

```bash
uv sync
```

Alternatively, create and activate a virtual environment manually, then install the dependencies listed in `pyproject.toml`.

## Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

The `.env` file is ignored by Git and should not be committed.

## Running the project

Run the main agent:

```bash
uv run main.py
```

Or activate the virtual environment and run Python directly:

```bash
source .venv/bin/activate
python main.py
```

Run the minimal weather-tool example:

```bash
uv run file_management.py
```

## How the code works

### `main.py`

`main.py` creates a LangChain agent with a terminal-command tool.

Simplified flow:

```text
User message
    → LangChain agent
        → decides whether to call terminal_command
            → executes shell command locally
            → returns stdout to the agent
    → final answer
```

Key components:

- `load_dotenv()` loads `OPENAI_API_KEY` and any other environment variables from `.env`.
- `terminal_command(command: str)` runs a shell command using `subprocess.run`.
- `create_agent(...)` creates the tool-calling agent.
- `agent.invoke(...)` sends a user message to the agent.

Current `main.py` prompt:

```python
result = agent.invoke(
    {"messages": [{"role": "user", "content": "create a documentation for the project"}]}
)
```

You can change the `content` value to ask the agent to perform a different task.

### `file_management.py`

`file_management.py` is a smaller example showing a single custom tool:

```python
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"
```

The agent can call this tool when asked about weather.

## Knowledge files

The `rag/` directory contains markdown files that can be used as local knowledge sources:

- `rag/sundaranbu.md` — profile, skills, education, experience, and contact details for Sundar Anbu.
- `rag/hasan.md` — profile, skills, and experience for C P Hasan.

The current `main.py` does not automatically read these files as RAG tools. To use them as an agentic RAG demo, add tools that read and return these markdown files.

Example:

```python
def read_sundaranbu_profile() -> str:
    """Read Sundar Anbu's profile from the local knowledge base."""
    return Path("rag/sundaranbu.md").read_text()


def read_hasan_profile() -> str:
    """Read C P Hasan's profile from the local knowledge base."""
    return Path("rag/hasan.md").read_text()
```

Then pass those functions in the `tools` list when creating the agent.

## Development notes

Dependencies are defined in `pyproject.toml`:

```toml
dependencies = [
    "dotenv>=0.9.9",
    "langchain>=1.4.1",
    "langchain-openai>=1.6.2",
]
```

The project is configured as a non-package uv project:

```toml
[tool.uv]
package = false
```

## Security considerations

The `terminal_command` tool in `main.py` is powerful and potentially dangerous because it runs arbitrary shell commands.

Recommended safeguards:

- Do not expose this agent as a public API without strict validation and sandboxing.
- Avoid running it with sensitive credentials available in the environment.
- Avoid running it from directories containing private files.
- Prefer an allowlist of safe commands if this is used beyond local experimentation.
- Review commands before execution if adding human-in-the-loop control.

## Troubleshooting

### Missing API key

If the OpenAI API key is missing, create `.env` with:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Model not found

`main.py` currently uses:

```python
model="openai:gpt-5.5"
```

If that model is unavailable for your account, replace it with a model you can access, for example:

```python
model="openai:gpt-4o-mini"
```

### Dependencies are not installed

Run:

```bash
uv sync
```

### Tool does not return errors

`terminal_command` currently returns only `stdout`. If a command fails, errors may be in `stderr`. For debugging, update the function to return both `stdout` and `stderr`.
