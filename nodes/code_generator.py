import asyncio
import os
from state import AgentState
from llm import llm
from prompts.code_generator import code_generator_prompt
from schemas.code_generator import CodeGeneratorOutput
from schemas.planner import PlannerOutput


def _read_file_contents(project_path: str, plan_json: str) -> str:
    plan = PlannerOutput.model_validate_json(plan_json)
    if not plan.files_to_modify:
        return "No existing files to modify."
    sections = []
    for file in plan.files_to_modify:
        full_path = os.path.join(project_path, file.path)
        if os.path.exists(full_path):
            with open(full_path, "r") as f:
                content = f.read()
            sections.append(f"### {file.path}\n{content}")
        else:
            sections.append(f"### {file.path}\n(file does not exist yet)")
    return "\n\n".join(sections)


async def code_generator(state: AgentState) -> dict:
    if state.get("error"):
        return {}
    if not state.get("plan"):
        return {
            "error": "code_generator: no plan in state",
            "logs": ["code_generator: failed — no plan available"],
        }
    try:
        plan = state["plan"] or ""
        project_structure = state["project_structure"] or ""
        file_contents = await asyncio.to_thread(
            _read_file_contents,
            state["project_path"],
            plan,
        )
        chain = code_generator_prompt | llm.with_structured_output(CodeGeneratorOutput)
        result: CodeGeneratorOutput = await chain.ainvoke({
            "project_path": state["project_path"],
            "project_structure": project_structure,
            "file_contents": file_contents,
            "plan": plan,
            "skills": state.get("skills") or "",
        })
        return {
            "generated_files": result.model_dump_json(indent=2),
            "logs": [f"code_generator: generated {len(result.files)} file(s)"],
        }
    except Exception as e:
        return {
            "error": f"code_generator: failed to generate code — {e}",
            "logs": ["code_generator: failed"],
        }
