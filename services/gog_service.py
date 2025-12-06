import requests
from typing import List
from models.models import SteamGame
import os
from dotenv import load_dotenv

load_dotenv()

GOG_CLIENT_ID = os.getenv("GOG_CLIENT_ID")
GOG_CLIENT_SECRET = os.getenv("GOG_CLIENT_SECRET")
# GOG_REDIRECT_URI = os.getenv("GOG_REDIRECT_URI")
GOG_API_BASE = os.getenv("GOG_API_BASE")
GOG_CODE = os.getenv("GOG_CODE")
GOG_REFRESH_TOKEN = os.getenv("GOG_REFRESH_TOKEN")


def refresh_gog_token() -> dict:
    url = "https://auth.gog.com/token"
    params = {
        "client_id": GOG_CLIENT_ID,
        "client_secret": GOG_CLIENT_SECRET,
        # "grant_type": "authorization_code",
        "grant_type": "refresh_token",
        "code": GOG_CODE,
        # "redirect_uri": GOG_REDIRECT_URI,
        "refresh_token": GOG_REFRESH_TOKEN,
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    return res.json().get("access_token", [])


def fetch_gog_games(access_token: str) -> List[SteamGame]:
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(
        "https://www.gog.com/account/getFilteredProducts?mediaType=1&sortBy=title",
        headers=headers,
    )
    res.raise_for_status()
    owned_products = res.json().get("products", [])

    if not owned_products:
        return []

    games: List[SteamGame] = []

    for p in owned_products:
        img = p.get("image", "")

        img = "https:" + img.lstrip("/")
        img += ".jpg"

        games.append(
            SteamGame(
                id=str(p.get("id")),
                title=p.get("title", "Unknown"),
                platform="GOG",
                image=img,
            )
        )
    return games
