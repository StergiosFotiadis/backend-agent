import json
from state import AgentState
from llm import llm
from prompts.security_reviewer import security_reviewer_prompt
from schemas.security_reviewer import SecurityReviewOutput
from schemas.code_generator import CodeGeneratorOutput


def _format_code_sections(generated_files_json: str) -> str:
    output = CodeGeneratorOutput.model_validate_json(generated_files_json)
    sections = [f"### {f.path}\n```python\n{f.content}\n```" for f in output.files]
    return "\n\n".join(sections)


async def security_reviewer(state: AgentState) -> dict:
    if state.get("error"):
        return {}
    if not state.get("generated_files"):
        return {
            "error": "security_reviewer: no generated files in state",
            "logs": ["security_reviewer: failed — no generated files available"],
        }
    try:
        generated_files: str = state["generated_files"]  # type: ignore[assignment]
        code = _format_code_sections(generated_files)
        skills = state.get("skills") or "No skill files loaded."

        chain = security_reviewer_prompt | llm.with_structured_output(SecurityReviewOutput)
        result: SecurityReviewOutput = await chain.ainvoke({
            "skills": skills,
            "code": code,
        })

        return {
            "generated_files": json.dumps(
                {"files": [f.model_dump() for f in result.files]}, indent=2
            ),
            "review_result": result.summary,
            "review_passed": True,
            "logs": [
                f"security_reviewer: reviewed {len(result.files)} file(s) — {len(result.changes_made)} change(s) made",
                *[f"  - {change}" for change in result.changes_made],
            ],
        }
    except Exception as e:
        return {
            "error": f"security_reviewer: failed — {e}",
            "logs": ["security_reviewer: failed"],
        }
