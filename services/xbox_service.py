import requests
from models.models import (
    XSTSAuthRequest,
    XSTSAuthResponse,
    XSTSAuthRequestProperties,
    TitleResponse,
    TitleDetailRequest,
    TitleDetailsRequestStats,
    TitleDetailResponse,
)
import os
from dotenv import load_dotenv

load_dotenv()

XBOX_XUID = os.getenv("XBOX_XUID")
XBOX_XUHS = os.getenv("XBOX_XUHS")
XBOX_XSTS_ENDPOINT = os.getenv("XBOX_XSTS_ENDPOINT")
XBOX_XSTS_RELYING_PARTY_RELYING_PARTY = os.getenv(
    "XBOX_XSTS_RELYING_PARTY_RELYING_PARTY"
)
XBOX_XSTS_USER_TOKENS = os.getenv("XBOX_XSTS_USER_TOKENS")
XBOX_GAME_HISTORY_ENDPOINT = os.getenv("XBOX_GAME_HISTORY_ENDPOINT")
XBOX_TITLE_DETAIL_ENDPOINT = os.getenv("XBOX_TITLE_DETAIL_ENDPOINT")


def refresh_xbox_token() -> XSTSAuthResponse:
    if (
        XBOX_XSTS_ENDPOINT is None
        or XBOX_XSTS_RELYING_PARTY_RELYING_PARTY is None
        or XBOX_XSTS_USER_TOKENS is None
    ):
        raise RuntimeError("Variabile d'ambiente non impostata.")

    data = XSTSAuthRequest(
        RelyingParty=XBOX_XSTS_RELYING_PARTY_RELYING_PARTY,
        TokenType="JWT",
        Properties=XSTSAuthRequestProperties(
            SandboxId="RETAIL",
            UserTokens=[XBOX_XSTS_USER_TOKENS],
        ),
    )

    headers = {
        "Content-Type": "application/json",
        "x-xbl-contract-version": "1",
    }

    res = requests.post(XBOX_XSTS_ENDPOINT, json=data.model_dump(), headers=headers)
    res.raise_for_status()
    return XSTSAuthResponse.model_validate(res.json())


def fetch_xbox_games(access_token: str) -> TitleResponse:
    if XBOX_GAME_HISTORY_ENDPOINT is None or XBOX_TITLE_DETAIL_ENDPOINT is None:
        raise RuntimeError("Variabile d'ambiente non impostata.")

    headers = {
        "x-xbl-contract-version": "2",
        "Accept-Language": "it-IT",
        "Authorization": f"XBL3.0 x={XBOX_XUHS};{access_token}",
    }
    res = requests.get(XBOX_GAME_HISTORY_ENDPOINT, headers=headers)
    res.raise_for_status()
    full_lib = TitleResponse.model_validate(res.json())
    my_lib = [
        game
        for game in full_lib.titles
        if any("Xbox" in device for device in game.devices)
    ]

    data = TitleDetailRequest(
        arrangebyfield="xuid",
        stats=[
            TitleDetailsRequestStats(name="MinutesPlayed", titleid=game.titleId)
            for game in my_lib
        ],
        xuids=[full_lib.xuid],
    )

    res = requests.post(
        XBOX_TITLE_DETAIL_ENDPOINT, headers=headers, json=data.model_dump()
    )
    res.raise_for_status()
    title_details = TitleDetailResponse.model_validate(res.json())

    played_title = [
        stat.titleid
        for statlistscollection in title_details.statlistscollection
        for stat in statlistscollection.stats
        if getattr(stat, "value") is not None
    ]

    for game in my_lib:
        if game.titleId not in played_title:
            my_lib.remove(game)

    return TitleResponse(xuid=full_lib.xuid, titles=my_lib)
