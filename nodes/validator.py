import os
from state import AgentState


async def validator(state: AgentState) -> dict:
    if not state.get("request", "").strip():
        return {
            "error": "Request cannot be empty.",
            "logs": ["validator: failed — request is empty"],
        }

    if not state.get("project_path", "").strip():
        return {
            "error": "Project path cannot be empty.",
            "logs": ["validator: failed — project path is empty"],
        }

    if not os.path.isdir(state["project_path"]):
        return {
            "error": f"Project path does not exist: {state['project_path']}",
            "logs": [f"validator: failed — path not found: {state['project_path']}"],
        }

    return {
        "error": None,
        "route": None,
        "project_structure": None,
        "plan": None,
        "skills": None,
        "generated_files": None,
        "review_result": None,
        "review_passed": None,
        "logs": ["validator: passed"],
    }
