# agentic-rag

A minimal **agentic RAG** demo: a LangChain agent chooses which knowledge file to read, then answers from that content.

This is intentionally simple — not production RAG. There is no vector store, embeddings, or chunking. Each tool returns a whole markdown file.

## How it works

1. You ask a question (e.g. “What is Hasan’s full name?”).
2. The agent (`create_agent`) decides which tool to call:
   - `sundaranbu` → reads `rag/sundaranbu.md`
   - `hasan` → reads `rag/hasan.md`
3. The tool returns the file text to the model.
4. The model answers using that context.

```
User question
    → Agent (gpt-4o-mini + tools)
        → sundaranbu / hasan tool
            → rag/*.md
        ← file contents
    ← final answer
```

## Project layout

```
agentic-rag/
├── main.py              # agent + tools
├── rag/
│   ├── sundaranbu.md    # knowledge about Sundar Anbu
│   └── hasan.md         # knowledge about C P Hasan
├── .env                 # OPENAI_API_KEY (not committed)
├── pyproject.toml
└── README.md
```

## Setup

Requires Python 3.14+ and [uv](https://github.com/astral-sh/uv).

```bash
uv sync
```

Create a `.env` in the project root:

```env
OPENAI_API_KEY=sk-...
```

## Run

Use the project venv (packages are installed there, not in system Python):

```bash
uv run main.py
# or
source .venv/bin/activate
python main.py
```

Change the question in `main.py`:

```python
result = agent.invoke({"messages": [("user", "your question here")]})
```

## Dependencies

- `langchain` — agent + tools
- `langchain-openai` — `ChatOpenAI`
- `dotenv` — load `.env`

## Notes

- `bind_tools` alone does not run tools; this project uses `create_agent`, which runs the tool loop.
- Agent input must be a messages dict, not a plain string:

  ```python
  agent.invoke({"messages": [("user", "...")]})
  ```
