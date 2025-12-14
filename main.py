from typing import List

from fastapi import Depends, FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader

from models.epic_models import TokenResponse
from models.gog_models import GogGame
from models.steam_models import SteamGame
from models.xbox_models import TitleResponse
from models.amazon_models import AMZGameResponse
from services.amazon_services import refresh_amazon_token, fetch_amazon_games
from services.gog_service import fetch_gog_games, refresh_gog_token
from services.steam_service import fetch_steam_games
from services.xbox_service import (
    fetch_xbox_games,
    xsts_token,
    refresh_token,
    auth_token,
)
from services.epic_services import (
    auth_code,
    fetch_epic_games,
)

app = FastAPI(title="Game Library API")
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=[
        "Authorization",
        "authorization",
        "Content-Type",
        "Accept",
        "nextToken",
        "nextCursor",
    ],
    expose_headers=["Authorization"],
)


# -----------------------------
# PERF: Endpoint Steam
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
# PERF: Endpoint GOG
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
# PERF: Endpoint Xbox
# -----------------------------
@app.post(
    "/xbox/token", tags=["Xbox"], summary="Richiesta Authorization: Bearer <token>"
)
def xbox_token():
    refresh = refresh_token()
    auth = auth_token(refresh.access_token)
    token_data = xsts_token(auth.Token)
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
def get_xbox_games(token: str = Depends(get_xbox_api_key), uhs: str = ""):
    return fetch_xbox_games(token, uhs)


# -----------------------------
# PERF: Endpoint Amazon
# -----------------------------
@app.post(
    "/amazon/token", tags=["Amazon"], summary="Richiesta Authorization: Bearer <token>"
)
def amazon_token():
    token_data = refresh_amazon_token()
    return token_data


api_key_header = APIKeyHeader(name="Authorization")


def get_amazon_api_key(api_key_header: str = Depends(api_key_header)) -> str:
    if not api_key_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    return api_key_header.replace("Bearer ", "")


def get_amazon_next_token(
    next_token: str | None = Header(None, alias="nextToken"),
) -> str | None:
    return next_token


@app.get(
    "/amazon/games",
    response_model=AMZGameResponse,
    tags=["Amazon"],
    summary="Restituisce la lista dei giochi Amazon dell'utente.",
)
def get_amazon_games(
    token: str = Depends(get_amazon_api_key),
    next_token: str = Depends(get_amazon_next_token),
):
    return fetch_amazon_games(token, next_token)


# -----------------------------
# PERF: Endpoint Epic
# -----------------------------
@app.post(
    "/epic/token",
    response_model=TokenResponse,
    tags=["Epic"],
    summary="Richiesta Authorization: Bearer <token>",
)
def epic_token():
    token_data = auth_code()
    return token_data


api_key_header = APIKeyHeader(name="Authorization")


def get_epic_api_key(api_key_header: str = Depends(api_key_header)) -> str:
    if not api_key_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    return api_key_header.replace("Bearer ", "")


def get_epic_next_cursor(
    next_cursor: str | None = Header(None, alias="nextCursor"),
) -> str | None:
    return next_cursor


@app.get(
    "/epic/games",
    tags=["Epic"],
    summary="Restituisce la lista dei giochi Epic dell'utente.",
)
def get_epic_games(
    token: str = Depends(get_epic_api_key),
    next_cursor: str = Depends(get_epic_next_cursor),
):
    return fetch_epic_games(token, next_cursor)
