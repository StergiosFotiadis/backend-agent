from typing import Literal
from pydantic import BaseModel


class RouterOutput(BaseModel):
    route: Literal["generate", "plan", "review"]
