from typing import List
from pydantic import BaseModel


class GeneratedFile(BaseModel):
    path: str
    content: str


class CodeGeneratorOutput(BaseModel):
    files: List[GeneratedFile]
