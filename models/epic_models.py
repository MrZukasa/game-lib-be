from typing import List, Optional
from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    expires_in: int
    expires_at: str
    token_type: str
    refresh_token: str
    refresh_expires: int
    refresh_expires_at: str
    account_id: str
    client_id: str
    internal_client: bool
    client_service: str
    scope: List
    displayName: str
    app: str
    in_app_id: str
    acr: str
    auth_time: str


class TokenRequest(BaseModel):
    grant_type: str
    code: str
    token_type: str


class ResponseMetadata(BaseModel):
    nextCursor: str
    stateToken: str


class Record(BaseModel):
    namespace: str
    catalogItemId: str
    appName: str
    country: str | None = None
    platform: List[str]
    productId: str
    sandboxName: str
    sandboxType: str
    recordType: str
    acquisitionDate: str
    dependencies: List | None = None


class EpicGameResponse(BaseModel):
    responseMetadata: ResponseMetadata
    records: List[Record]


class AuthCodeResponse(BaseModel):
    warning: str
    redirectUrl: str
    authorizationCode: Optional[str]
    exchangeCode: Optional[str]
    sid: Optional[str]
