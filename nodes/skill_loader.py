import asyncio
import os
from state import AgentState
from config import SKILLS_PATH


def _load_skills(path: str) -> str:
    if not os.path.isdir(path):
        return ""
    skills = []
    for filename in sorted(os.listdir(path)):
        if filename.endswith(".md"):
            filepath = os.path.join(path, filename)
            with open(filepath, "r") as f:
                skills.append(f"# {filename}\n{f.read()}")
    return "\n\n".join(skills)


async def skill_loader(state: AgentState) -> dict:
    if state.get("error"):
        return {}
    try:
        skills = await asyncio.to_thread(_load_skills, SKILLS_PATH)
        if not skills:
            return {
                "skills": "",
                "logs": ["skill_loader: no skill files found, proceeding without skills"],
            }
        return {
            "skills": skills,
            "logs": [f"skill_loader: loaded skills from {SKILLS_PATH}"],
        }
    except Exception as e:
        return {
            "error": f"skill_loader: failed to load skills — {e}",
            "logs": ["skill_loader: failed"],
        }
