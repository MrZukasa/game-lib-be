from pydantic import BaseModel, Field
from typing import List, Any


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
    type_: str | None = Field(None, alias="__type")
    channelId: str | None = None
    entitlementDateFromEpoch: str
    id: str
    lastModifiedDate: float
    product: Product
    signature: str
    state: str


class AMZGameResponse(BaseModel):
    entitlements: List[Entitlement]
    nextToken: str | None = None
