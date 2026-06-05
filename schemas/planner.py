from typing import List
from pydantic import BaseModel


class FileToCreate(BaseModel):
    path: str
    purpose: str


class FileToModify(BaseModel):
    path: str
    changes: str


class PlannerOutput(BaseModel):
    files_to_create: List[FileToCreate]
    files_to_modify: List[FileToModify]
    summary: str
