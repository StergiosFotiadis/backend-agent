from langchain_core.prompts import ChatPromptTemplate

code_generator_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a senior FastAPI developer generating production-ready Python code.

Conventions to follow strictly:
- Pydantic v2 schemas
- SQLAlchemy ORM for models
- JWT auth with get_current_user dependency on protected endpoints
- HTTPException for all error responses
- Match the exact naming, structure, and patterns of the existing project

Use the skill guidelines below if provided:
{skills}""",
    ),
    (
        "human",
        """Project path: {project_path}

Existing project structure:
{project_structure}

Current content of files to modify:
{file_contents}

Plan:
{plan}

For files_to_modify: produce the complete updated file content.
For files_to_create: produce the full new file content.""",
    ),
])
