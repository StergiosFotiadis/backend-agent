from typing import List
from pydantic import BaseModel


class SecurityReviewOutput(BaseModel):
    passed: bool
    issues: List[str]
    summary: str
