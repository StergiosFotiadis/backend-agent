import asyncio
import json
import os
from state import AgentState


def _write_files(project_path: str, generated_files_json: str) -> list[str]:
    data = json.loads(generated_files_json)
    written = []
    for file in data["files"]:
        full_path = os.path.join(project_path, file["path"])
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(file["content"])
        written.append(file["path"])
    return written


async def output_writer(state: AgentState) -> dict:
    if state.get("error"):
        return {}
    if not state.get("generated_files"):
        return {
            "error": "output_writer: no files to write",
            "logs": ["output_writer: failed — no generated files in state"],
        }
    try:
        written = await asyncio.to_thread(
            _write_files,
            state["project_path"],
            state["generated_files"],  # type: ignore[arg-type]
        )
        return {
            "logs": [
                f"output_writer: wrote {len(written)} file(s) to {state['project_path']}",
                *[f"  - {path}" for path in written],
            ]
        }
    except Exception as e:
        return {
            "error": f"output_writer: failed to write files — {e}",
            "logs": ["output_writer: failed"],
        }
