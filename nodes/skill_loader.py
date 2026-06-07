import base64
import httpx
from state import AgentState
from config import GITHUB_TOKEN, GITHUB_REPO, SKILLS_GITHUB_PATH


async def _fetch_skills_from_github() -> str:
    if not GITHUB_TOKEN:
        return ""

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    encoded_path = SKILLS_GITHUB_PATH.replace(" ", "%20")
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{encoded_path}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        items = resp.json()

        skills = []
        for item in sorted(items, key=lambda x: x["name"]):
            if item["type"] == "file" and item["name"].endswith(".md"):
                file_resp = await client.get(item["url"], headers=headers)
                file_resp.raise_for_status()
                content = base64.b64decode(file_resp.json()["content"]).decode("utf-8")
                skills.append(f"# {item['name']}\n{content}")

    return "\n\n".join(skills)


async def skill_loader(state: AgentState) -> dict:
    if state.get("error"):
        return {}
    try:
        skills = await _fetch_skills_from_github()
        if not skills:
            return {
                "skills": "",
                "logs": ["skill_loader: no skill files found, proceeding without skills"],
            }
        return {
            "skills": skills,
            "logs": [f"skill_loader: loaded skills from {GITHUB_REPO}/{SKILLS_GITHUB_PATH}"],
        }
    except Exception as e:
        return {
            "error": f"skill_loader: failed to load skills — {e}",
            "logs": ["skill_loader: failed"],
        }
