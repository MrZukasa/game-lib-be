import requests
from models.xbox_models import (
    RefreshTokenResponse,
    RefreshTokenRequest,
    AuthTokenResponse,
    AuthTokenRequest,
    Properties,
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

XBOX_CLIENT_ID = os.getenv("XBOX_CLIENT_ID")
XBOX_REDIRECT_URI = os.getenv("XBOX_REDIRECT_URI")
XBOX_XSTS_ENDPOINT = os.getenv("XBOX_XSTS_ENDPOINT")
XBOX_REFRESH_TOKEN = os.getenv("XBOX_REFRESH_TOKEN")
XBOX_AUTH_ENDPOINT = os.getenv("XBOX_AUTH_ENDPOINT")
XBOX_GAME_HISTORY_ENDPOINT = os.getenv("XBOX_GAME_HISTORY_ENDPOINT")
XBOX_TITLE_DETAIL_ENDPOINT = os.getenv("XBOX_TITLE_DETAIL_ENDPOINT")
XBOX_REFRESH_TOKEN_ENDPOINT = os.getenv("XBOX_REFRESH_TOKEN_ENDPOINT")


def refresh_token() -> RefreshTokenResponse:
    if (
        XBOX_REFRESH_TOKEN_ENDPOINT is None
        or XBOX_CLIENT_ID is None
        or XBOX_REDIRECT_URI is None
        or XBOX_REFRESH_TOKEN is None
    ):
        raise RuntimeError("Variabile d'ambiente non impostata.")

    data = RefreshTokenRequest(
        scope="Xboxlive.signin Xboxlive.offline_access",
        client_id=XBOX_CLIENT_ID,
        redirect_uri=XBOX_REDIRECT_URI,
        grant_type="refresh_token",
        refresh_token=XBOX_REFRESH_TOKEN,
    )

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    form_data = data.model_dump()

    res = requests.post(XBOX_REFRESH_TOKEN_ENDPOINT, data=form_data, headers=headers)
    res.raise_for_status()
    return RefreshTokenResponse.model_validate(res.json())


def auth_token(refresh_token: str) -> AuthTokenResponse:
    if XBOX_AUTH_ENDPOINT is None:
        raise RuntimeError("Variabile d'ambiente non impostata.")

    data = AuthTokenRequest(
        RelyingParty="http://auth.xboxlive.com",
        TokenType="JWT",
        Properties=Properties(
            AuthMethod="RPS",
            SiteName="user.auth.xboxlive.com",
            RpsTicket=f"d={refresh_token}",
        ),
    )

    headers = {
        "Content-Type": "application/json",
        "x-xbl-contract-version": "1",
    }

    res = requests.post(XBOX_AUTH_ENDPOINT, json=data.model_dump(), headers=headers)
    res.raise_for_status()
    return AuthTokenResponse.model_validate(res.json())


def xsts_token(auth_token: str) -> XSTSAuthResponse:
    if XBOX_XSTS_ENDPOINT is None:
        raise RuntimeError("Variabile d'ambiente non impostata.")

    data = XSTSAuthRequest(
        RelyingParty="http://xboxlive.com",
        TokenType="JWT",
        Properties=XSTSAuthRequestProperties(
            SandboxId="RETAIL",
            UserTokens=[auth_token],
        ),
    )

    headers = {
        "Content-Type": "application/json",
        "x-xbl-contract-version": "1",
    }

    res = requests.post(XBOX_XSTS_ENDPOINT, json=data.model_dump(), headers=headers)
    res.raise_for_status()
    return XSTSAuthResponse.model_validate(res.json())


def fetch_xbox_games(access_token: str, uhs: str) -> TitleResponse:
    if XBOX_GAME_HISTORY_ENDPOINT is None or XBOX_TITLE_DETAIL_ENDPOINT is None:
        raise RuntimeError("Variabile d'ambiente non impostata.")

    headers = {
        "x-xbl-contract-version": "2",
        "Accept-Language": "it-IT",
        "Authorization": f"XBL3.0 x={uhs};{access_token}",
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
