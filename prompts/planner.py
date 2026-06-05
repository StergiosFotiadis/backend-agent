from langchain_core.prompts import ChatPromptTemplate

planner_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a senior FastAPI developer planning code changes for an existing project.

Analyze the project structure and user request, then produce a precise plan.
Follow the existing project's naming conventions and folder structure exactly.""",
    ),
    (
        "human",
        """Project path: {project_path}

Project structure:
{project_structure}

User request: {request}""",
    ),
])
