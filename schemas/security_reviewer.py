from typing import List
from pydantic import BaseModel
from schemas.code_generator import GeneratedFile


class SecurityReviewOutput(BaseModel):
    files: List[GeneratedFile]
    changes_made: List[str]
    summary: str
