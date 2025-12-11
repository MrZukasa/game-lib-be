from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class Properties(BaseModel):
    AuthMethod: str
    SiteName: str
    RpsTicket: str


class AuthTokenRequest(BaseModel):
    RelyingParty: str
    TokenType: str
    Properties: Properties


class XuiItem(BaseModel):
    uhs: str


class DisplayClaims(BaseModel):
    xui: List[XuiItem]


class AuthTokenResponse(BaseModel):
    IssueInstant: str
    NotAfter: str
    Token: str
    DisplayClaims: DisplayClaims


class RefreshTokenRequest(BaseModel):
    scope: str
    client_id: str
    redirect_uri: str
    grant_type: str
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    token_type: str
    expires_in: int
    scope: str
    access_token: str
    refresh_token: str
    user_id: str


class XSTSAuthRequestProperties(BaseModel):
    SandboxId: str
    UserTokens: List[str]


class XSTSAuthRequest(BaseModel):
    RelyingParty: str
    TokenType: str
    Properties: XSTSAuthRequestProperties


class XSTSAuthResponseXuiItem(BaseModel):
    gtg: str
    xid: str
    uhs: str


class XSTSAuthResponseDisplayClaims(BaseModel):
    xui: List[XSTSAuthResponseXuiItem]


class XSTSAuthResponse(BaseModel):
    IssueInstant: str
    NotAfter: str
    Token: str
    DisplayClaims: XSTSAuthResponseDisplayClaims


class TitleDetail(BaseModel):
    description: str
    developerName: str
    genres: List[str]
    minAge: int
    publisherName: str
    releaseDate: Optional[str]
    shortDescription: Optional[str]


class XboxGame(BaseModel):
    titleId: str
    pfn: Optional[str]
    name: str
    type: str
    devices: List[str]
    displayImage: str
    detail: TitleDetail


class TitleResponse(BaseModel):
    xuid: str
    titles: List[XboxGame]


class TitleDetailsRequestStats(BaseModel):
    name: str
    titleid: str


class TitleDetailRequest(BaseModel):
    arrangebyfield: str
    stats: List[TitleDetailsRequestStats]
    xuids: List[str]


class TitleDetailStat(BaseModel):
    groupproperties: Dict[str, Any]
    xuid: str
    scid: str
    titleid: str
    name: str
    type: str
    properties: Dict[str, Any]
    value: Optional[str] = None


class StatlistscollectionItem(BaseModel):
    arrangebyfield: str
    arrangebyfieldid: str
    stats: List[TitleDetailStat]


class TitleDetailResponse(BaseModel):
    groups: List
    statlistscollection: List[StatlistscollectionItem]
