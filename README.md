# Backend Agent

An autonomous backend developer agent built with LangGraph that receives a natural language request and generates production-ready FastAPI code — then pauses for human approval before writing anything to disk.

## What it does

- Accepts a natural language request + target project path
- Routes intelligently between `generate`, `plan`, and `review` pipelines
- Reads the existing project structure before touching anything
- Loads coding style from local `skills/*.md` files
- Plans, generates, and security-reviews FastAPI code (Pydantic v2, SQLAlchemy ORM, JWT auth)
- Interrupts before writing — human must approve before any file is written

## Architecture

```
START → validator → router → planner → skill_loader → code_generator → security_reviewer → [INTERRUPT] → output_writer → END
```

Conditional edges handle errors at every step and route cleanly between `generate`, `plan`, and `review` flows.

## Tech stack

- [LangGraph](https://github.com/langchain-ai/langgraph) — stateful agent graph with human-in-the-loop interrupt
- [LangChain Anthropic](https://python.langchain.com/docs/integrations/chat/anthropic/) — `claude-sonnet-4-6`, structured output via Pydantic
- [FastAPI](https://fastapi.tiangolo.com/) — target framework for all generated code
- Pydantic v2, SQLAlchemy ORM, JWT auth patterns

## Project structure

```
backend-agent/
├── agent.py              # graph wiring and compile
├── state.py              # GraphInput + AgentState
├── llm.py                # shared LLM instance
├── config.py             # model config constants
├── nodes/                # one file per graph node
├── schemas/              # Pydantic structured output schemas
├── prompts/              # ChatPromptTemplates separated from node logic
├── skills/               # .md coding style files (add your own)
├── .env.example          # required environment variables
└── pyproject.toml
```

## Setup

```bash
# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Fill in ANTHROPIC_API_KEY and optionally LANGCHAIN_API_KEY
```

## Running

```bash
# Start the LangGraph API server
langgraph dev
```

Then open **LangGraph Studio** and submit a request with:
- `request` — what you want built (e.g. `"add a POST /products endpoint"`)
- `project_path` — absolute path to your FastAPI project

## Skills

Drop `.md` files into `skills/` to teach the agent your project's coding conventions. The agent loads them alphabetically and passes them to the code generator as context.

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key |
| `LANGCHAIN_TRACING_V2` | No | Enable LangSmith tracing |
| `LANGCHAIN_PROJECT` | No | LangSmith project name |
| `LANGCHAIN_API_KEY` | No | LangSmith API key |
