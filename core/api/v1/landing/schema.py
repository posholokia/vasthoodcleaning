from typing import (
    Annotated,
    Optional,
)

from annotated_types import (
    MaxLen,
    MinLen,
)
from ninja import Schema
from pydantic import Field


class MainScreenRetrieveSchema(Schema):
    title: Annotated[str, MinLen(1), MaxLen(100)]
    text: str
    subtext: str


class AdvantageRetrieveSchema(Schema):
    title: Annotated[str, MinLen(1), MaxLen(100)]
    text: Annotated[str, MinLen(1)]


class FontColorRetrieveSchema(Schema):
    color: str


class ServiceRetrieveSchema(Schema):
    id: int
    name: Annotated[str, MinLen(1), MaxLen(100)]
    font_color: FontColorRetrieveSchema
    discount_message: Annotated[str, MinLen(1), MaxLen(100)]
    image: str


class ServiceDetailRetrieveSchema(Schema):
    service: ServiceRetrieveSchema
    quality_title: Annotated[str, MinLen(1), MaxLen(100)]
    quality_text: Annotated[str, MinLen(1)]
    advantage: list[AdvantageRetrieveSchema] = Field(default_factory=list)


class AboutBlockRetrieveSchema(Schema):
    first_title: Annotated[str, MinLen(1), MaxLen(100)]
    first_description: Annotated[str, MinLen(1)]
    second_title: Annotated[str, MinLen(1), MaxLen(100)]
    second_description: Annotated[str, MinLen(1)]


class AboutRetrieveSchema(Schema):
    title: Annotated[str, MinLen(1), MaxLen(100)]
    text: Annotated[str, MinLen(1)]
    blocks: list[AboutBlockRetrieveSchema] = Field(default_factory=list)


class ResultPhotoRetrieveSchema(Schema):
    image: str


class ResultRetrieveSchema(Schema):
    description: Annotated[str, MinLen(1)]
    result_photos: list[ResultPhotoRetrieveSchema] = Field(
        default_factory=list
    )


class FooterRetrieveSchema(Schema):
    email: Annotated[str, MinLen(3), MaxLen(254)]
    operating_mode: Annotated[str, MinLen(1), MaxLen(32)]
    address: Annotated[str, MinLen(1), MaxLen(64)]


class FAQRetrieveSchema(Schema):
    title: str
    question: str
    answer: str


class SiteRetrieveSchema(Schema):
    whatsapp: Annotated[str, MinLen(1), MaxLen(16)]
    phone: str
    about: Optional[AboutRetrieveSchema] = None
    results: Optional[ResultRetrieveSchema] = None
    services: list[ServiceRetrieveSchema] = Field(default_factory=list)
    main_screen: Optional[MainScreenRetrieveSchema] = None
    faq: Optional[FAQRetrieveSchema] = None
    footer: Optional[FooterRetrieveSchema] = None
