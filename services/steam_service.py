from typing import List
import os
from dotenv import load_dotenv
import requests
from models.steam_models import SteamGame

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")


def fetch_steam_games() -> List[SteamGame]:
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": STEAM_ID,
        "include_appinfo": True,
        "format": "json",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    games_data = data.get("response", {}).get("games", [])

    return [
        SteamGame(
            id=str(game["appid"]),
            title=game["name"],
            platform="Steam",
            image=f"https://cdn.cloudflare.steamstatic.com/steam/apps/{game['appid']}/header.jpg",
        )
        for game in games_data
    ]
