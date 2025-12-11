import requests
from models.amazon_models import (
    AMZTokenRequest,
    AMZTokenResponse,
    AMZGameRequest,
    AMZGameResponse,
)
import os
from dotenv import load_dotenv

load_dotenv()

AMZ_SOURCE_TOKEN = os.getenv("AMZ_SOURCE_TOKEN")
AMZ_TITLE_ENDPOINT = os.getenv("AMZ_TITLE_ENDPOINT")
AMZ_TOKEN_ENDPOINT = os.getenv("AMZ_TOKEN_ENDPOINT")
AMZ_TITLE_KEY_ID = os.getenv("AMZ_TITLE_KEY_ID")
AMZ_HW_HASH = os.getenv("AMZ_HW_HASH")
AMZ_HEADER_CONTENT_ENCODING = os.getenv("AMZ_HEADER_CONTENT_ENCODING")
AMZ_HEADER_X_AMZ_TARGET = os.getenv("AMZ_HEADER_X_AMZ_TARGET")


def refresh_amazon_token() -> AMZTokenResponse:
    if AMZ_TOKEN_ENDPOINT is None or AMZ_SOURCE_TOKEN is None:
        raise RuntimeError("Variabile d'ambiente non impostata.")

    data = AMZTokenRequest(
        source_token_type="refresh_token",
        requested_token_type="access_token",
        source_token=AMZ_SOURCE_TOKEN,
        app_name="AGSLauncher",
        app_version="3.0.9778.3",
    )

    res = requests.post(AMZ_TOKEN_ENDPOINT, json=data.model_dump())
    res.raise_for_status()
    return AMZTokenResponse.model_validate(res.json())


def fetch_amazon_games(
    access_token: str, next_token: str | None = None
) -> AMZGameResponse:
    if AMZ_TITLE_ENDPOINT is None or AMZ_TITLE_KEY_ID is None or AMZ_HW_HASH is None:
        raise RuntimeError("Variabile d'ambiente non impostata.")

    data = AMZGameRequest(
        clientId="Sonic",
        syncPoint=None,
        nextToken=next_token,
        maxResults=50,
        productIdFilter=None,
        keyId=AMZ_TITLE_KEY_ID,
        hardwareHash=AMZ_HW_HASH,
        disableStateFilter=False,
        Operation="GetEntitlements",
    )

    headers = {
        "Content-Encoding": "amz-1.0",
        "X-Amz-Target": "com.amazon.animusdistributionservice.entitlement.AnimusEntitlementsService.GetEntitlements",
        "x-amzn-token": access_token,
    }

    res = requests.post(AMZ_TITLE_ENDPOINT, headers=headers, json=data.model_dump())
    res.raise_for_status()
    return AMZGameResponse.model_validate(res.json())
