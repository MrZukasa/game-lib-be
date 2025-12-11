from pydantic import BaseModel
from typing import Optional


# PERF: GOG MODELS
class GogGame(BaseModel):
    id: str
    title: str
    platform: str
    image: Optional[str]
