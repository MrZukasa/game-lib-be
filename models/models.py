from pydantic import BaseModel
from typing import List, Optional


class SteamGame(BaseModel):
    id: str
    title: str
    platform: str
    image: Optional[str]


class SteamOwnedGamesResponse(BaseModel):
    games: List[SteamGame]


class GogCodeRequest(BaseModel):
    code: str
