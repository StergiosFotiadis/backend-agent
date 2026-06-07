import asyncio
import os
from state import AgentState
from llm import llm
from prompts.planner import planner_prompt
from schemas.planner import PlannerOutput


def _scan_project(path: str) -> str:
    skip = {"__pycache__", ".git", ".venv", "node_modules"}
    lines = []
    for root, dirs, files in os.walk(path):
        dirs[:] = sorted([d for d in dirs if d not in skip])
        level = root.replace(path, "").count(os.sep)
        indent = "  " * level
        lines.append(f"{indent}{os.path.basename(root)}/")
        for file in sorted(files):
            if not file.endswith(".pyc"):
                lines.append(f"{indent}  {file}")
    return "\n".join(lines)


async def planner(state: AgentState) -> dict:
    if state.get("error"):
        return {}
    try:
        project_structure = await asyncio.to_thread(
            _scan_project, state["project_path"]
        )
        chain = planner_prompt | llm.with_structured_output(PlannerOutput)
        result: PlannerOutput = await chain.ainvoke(
            {
                "project_path": state["project_path"],
                "project_structure": project_structure,
                "request": state["request"],
            }
        )
        return {
            "project_structure": project_structure,
            "plan": result.model_dump_json(indent=2),
            "logs": [
                f"planner: {len(result.files_to_create)} file(s) to create, "
                f"{len(result.files_to_modify)} to modify — {result.summary}"
            ],
        }
    except Exception as e:
        return {
            "error": f"planner: failed to generate plan — {e}",
            "logs": ["planner: failed"],
        }
