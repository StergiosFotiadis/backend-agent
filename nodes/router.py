from state import AgentState
from llm import llm
from prompts.router import router_prompt
from schemas.router import RouterOutput


async def router(state: AgentState) -> dict:
    try:
        chain = router_prompt | llm.with_structured_output(RouterOutput)
        result: RouterOutput = await chain.ainvoke({"request": state["request"]})
        return {
            "route": result.route,
            "logs": [f"router: classified as '{result.route}'"],
        }
    except Exception as e:
        return {
            "error": f"router: failed to classify request — {e}",
            "logs": ["router: failed"],
        }
