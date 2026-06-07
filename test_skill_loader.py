import asyncio
from dotenv import load_dotenv
load_dotenv()
from nodes.skill_loader import _fetch_skills_from_github

async def main():
    skills = await _fetch_skills_from_github()
    if not skills:
        print("No skills loaded — check GITHUB_TOKEN and repo path")
        return
    headers = [l for l in skills.splitlines() if l.startswith("# ")]
    print(f"Loaded {len(headers)} skill files:\n")
    for h in headers:
        print(h)

asyncio.run(main())
