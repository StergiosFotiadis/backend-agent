from langgraph.graph import StateGraph, START, END

from state import AgentState, GraphInput
from nodes.validator import validator
from nodes.router import router
from nodes.planner import planner
from nodes.skill_loader import skill_loader
from nodes.code_generator import code_generator
from nodes.security_reviewer import security_reviewer
from nodes.output_writer import output_writer


def route_after_validation(state: AgentState) -> str:
    if state.get("error"):
        return END
    return "router"


def route_after_plan(state: AgentState) -> str:
    if state.get("error"):
        return END
    route = state.get("route", "generate")
    if route == "plan":
        return END
    if route == "review":
        return "security_reviewer"
    return "skill_loader"


def route_after_review(state: AgentState) -> str:
    if state.get("error"):
        return END
    if state.get("review_passed"):
        return "output_writer"
    return END


builder = StateGraph(AgentState, input=GraphInput)

builder.add_node("validator", validator)
builder.add_node("router", router)
builder.add_node("planner", planner)
builder.add_node("skill_loader", skill_loader)
builder.add_node("code_generator", code_generator)
builder.add_node("security_reviewer", security_reviewer)
builder.add_node("output_writer", output_writer)

builder.add_edge(START, "validator")
builder.add_conditional_edges("validator", route_after_validation, {
    "router": "router",
    END: END,
})
builder.add_edge("router", "planner")
builder.add_conditional_edges("planner", route_after_plan, {
    "skill_loader": "skill_loader",
    "security_reviewer": "security_reviewer",
    END: END,
})
builder.add_edge("skill_loader", "code_generator")
builder.add_edge("code_generator", "security_reviewer")
builder.add_conditional_edges("security_reviewer", route_after_review, {
    "output_writer": "output_writer",
    END: END,
})
builder.add_edge("output_writer", END)

graph = builder.compile(interrupt_before=["output_writer"])
