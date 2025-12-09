from fastapi import HTTPException, FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from typing import List

from models.models import SteamGame, GogGame, TitleResponse
from services.gog_service import refresh_gog_token, fetch_gog_games
from services.steam_service import fetch_steam_games
from services.xbox_service import refresh_xbox_token, fetch_xbox_games

app = FastAPI(title="Game Library API")
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "authorization", "Content-Type", "Accept"],
    expose_headers=["Authorization"],
)


# -----------------------------
# Endpoint Steam
# -----------------------------
@app.get(
    "/steam/games",
    response_model=List[SteamGame],
    tags=["Steam"],
    summary="Restituisce la lista dei giochi Steam dell'utente.",
)
def get_steam_games():
    return fetch_steam_games()


# -----------------------------
# Endpoint GOG
# -----------------------------
@app.post(
    "/gog/token",
    tags=["GOG"],
    summary="Richiesta Authorization: Bearer <token>",
)
def gog_token():
    token_data = refresh_gog_token()
    return token_data


api_key_header = APIKeyHeader(name="Authorization")


def get_gog_api_key(api_key_header: str = Depends(api_key_header)) -> str:
    if not api_key_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if not api_key_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Wrong Authorization format")
    return api_key_header.replace("Bearer ", "")


@app.get(
    "/gog/games",
    response_model=List[GogGame],
    tags=["GOG"],
    summary="Restituisce la lista dei giochi GOG dell'utente.",
)
def get_gog_games(token: str = Depends(get_gog_api_key)):
    return fetch_gog_games(token)


# -----------------------------
# Endpoint Xbox
# -----------------------------
@app.post(
    "/xbox/token", tags=["Xbox"], summary="Richiesta Authorization: Bearer <token>"
)
def xbox_token():
    token_data = refresh_xbox_token()
    return token_data


api_key_header = APIKeyHeader(name="Authorization")


def get_xbox_api_key(api_key_header: str = Depends(api_key_header)) -> str:
    if not api_key_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    return api_key_header.replace("Bearer ", "")


@app.get(
    "/xbox/games",
    response_model=TitleResponse,
    tags=["Xbox"],
    summary="Restituisce la lista dei giochi Xbox dell'utente.",
)
def get_xbox_games(token: str = Depends(get_xbox_api_key)):
    return fetch_xbox_games(token)
