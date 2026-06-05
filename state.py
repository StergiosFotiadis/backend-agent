import operator
from typing import Annotated, Optional
from typing_extensions import TypedDict
from pydantic import BaseModel


class GraphInput(BaseModel):
    request: str
    project_path: str


class AgentState(TypedDict):
    request: str
    project_path: str
    route: Optional[str]
    project_structure: Optional[str]
    plan: Optional[str]
    skills: Optional[str]
    generated_files: Optional[str]
    review_result: Optional[str]
    review_passed: Optional[bool]
    error: Optional[str]
    logs: Annotated[list, operator.add]
