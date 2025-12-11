from pydantic import BaseModel
from typing import Optional


# PERF: STEAM MODELS
class SteamGame(BaseModel):
    id: str
    title: str
    platform: str
    image: Optional[str]
