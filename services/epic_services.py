import requests
import os
from models.epic_models import (
    TokenRequest,
    TokenResponse,
    EpicGameResponse,
    AuthCodeResponse,
)
from dotenv import load_dotenv

load_dotenv()

EPIC_TOKEN_ENDPOINT = os.getenv("EPIC_TOKEN_ENDPOINT")
EPIC_GAME_ENDPOINT = os.getenv("EPIC_GAME_ENDPOINT")
EPIC_BASIC_TOKEN = os.getenv("EPIC_BASIC_TOKEN")
EPIC_GAME_DETAILS_ENDPOINT = os.getenv("EPIC_GAME_DETAILS_ENDPOINT")
EPIC_COOKIE = os.getenv("EPIC_COOKIE")
EPIC_AUTH_CODE_ENDPOINT = os.getenv("EPIC_AUTH_CODE_ENDPOINT")


def auth_code() -> TokenResponse:
    if EPIC_COOKIE is None or EPIC_AUTH_CODE_ENDPOINT is None:
        raise RuntimeError("Variabile d'ambiente non impostata.")
    headers = {"Cookie": EPIC_COOKIE}

    res = requests.get(EPIC_AUTH_CODE_ENDPOINT, headers=headers)
    res.raise_for_status()
    auth_code_response = AuthCodeResponse.model_validate(res.json())
    if auth_code_response.authorizationCode is not None:
        token_response = get_epic_token(auth_code_response.authorizationCode)
        return token_response
    else:
        raise RuntimeError("Non è stato possibile ottenere il token")


def get_epic_token(authorization_code: str) -> TokenResponse:
    if EPIC_TOKEN_ENDPOINT is None:
        raise RuntimeError("Variabile d'ambiente non impostata.")

    data = TokenRequest(
        grant_type="authorization_code",
        code=authorization_code,
        token_type="eg1",
    )

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {EPIC_BASIC_TOKEN}",
    }

    form_data = data.model_dump()

    res = requests.post(EPIC_TOKEN_ENDPOINT, data=form_data, headers=headers)
    res.raise_for_status()
    return TokenResponse.model_validate(res.json())


def fetch_epic_games(
    access_token: str, next_cursor: str | None = None
) -> dict[str, dict]:
    if EPIC_GAME_ENDPOINT is None:
        raise RuntimeError("Variabile d'ambiente non impostata.")

    params = {}
    if next_cursor is not None:
        params["cursor"] = next_cursor

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    res = requests.get(EPIC_GAME_ENDPOINT, headers=headers, params=params)
    res.raise_for_status()
    products = EpicGameResponse.model_validate(res.json())

    game_details: dict[str, dict] = {}
    game_details.update(products.responseMetadata)
    for record in products.records:
        catalog_item_id = record.catalogItemId
        details = fetch_game_details(access_token, record.namespace, catalog_item_id)
        game_details["record"] = details[catalog_item_id]
    return game_details


def fetch_game_details(access_token: str, namespace: str, item_id: str) -> dict:
    if EPIC_GAME_DETAILS_ENDPOINT is None:
        raise RuntimeError("Variabile d'ambiente non impostata.")

    params = {"id": item_id}

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    URL = f"{EPIC_GAME_DETAILS_ENDPOINT}{namespace}/bulk/items"

    res = requests.get(URL, params=params, headers=headers)
    res.raise_for_status()
    return res.json()
