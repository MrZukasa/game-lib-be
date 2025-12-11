from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict


# PERF: STEAM MODELS
class SteamGame(BaseModel):
    id: str
    title: str
    platform: str
    image: Optional[str]


# PERF: GOG MODELS
class GogGame(BaseModel):
    id: str
    title: str
    platform: str
    image: Optional[str]


# PERF: XBOX MODELS
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


# PERF: AMAZON MODELS
class AMZTokenRequest(BaseModel):
    source_token_type: str
    requested_token_type: str
    source_token: str
    app_name: str
    app_version: str


class AgeClassification(BaseModel):
    age_classification: str


class Response(BaseModel):
    token_expires_in: str
    token_type: str
    token: str


class AMZTokenResponse(BaseModel):
    access_token: str
    age_classification: AgeClassification
    response: Response
    token_type: str
    expires_in: int
    request_id: str


class AMZGameRequest(BaseModel):
    clientId: str
    syncPoint: Any
    nextToken: Any
    maxResults: int
    productIdFilter: Any
    keyId: str
    hardwareHash: str
    disableStateFilter: bool
    Operation: str


class Websites(BaseModel):
    OFFICIAL: str


class Details(BaseModel):
    backgroundUrl1: str
    backgroundUrl2: str
    developer: str
    esrbRating: str
    gameModes: List[str]
    genres: List[str]
    keywords: List[str]
    legacyProductIds: List[str] | None = None
    logoUrl: str
    otherDevelopers: List
    pegiRating: str
    pgCrownImageUrl: str
    publisher: str
    releaseDate: str
    screenshots: List
    shortDescription: str | None = None
    uskRating: str
    websites: Websites


class ProductDetail(BaseModel):
    details: Details
    iconUrl: str


class Product(BaseModel):
    asinVersion: int
    description: str
    domainId: str
    id: str
    productDetail: ProductDetail
    productLine: str
    sku: str
    title: str
    vendorId: str


class Entitlement(BaseModel):
    type_: str = Field(alias="__type")
    channelId: str
    entitlementDateFromEpoch: str
    id: str
    lastModifiedDate: float
    product: Product
    signature: str
    state: str


class AMZGameResponse(BaseModel):
    entitlements: List[Entitlement]
    nextToken: str
