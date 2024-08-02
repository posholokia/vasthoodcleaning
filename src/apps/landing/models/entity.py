from dataclasses import (
    dataclass,
    field,
)
from enum import Enum
from typing import (
    Annotated,
    Optional,
)

from annotated_types import (
    MaxLen,
    MinLen,
)


class ColorFontEnum(Enum):
    white = "#FFFFFF"
    black = "#000000"


@dataclass
class MainScreenEntity:
    id: int
    title: Annotated[str, MinLen(1), MaxLen(100)]  # заголовок
    text: str = ""  # над заголовком
    subtext: str = ""  # под заголовком


@dataclass
class AdvantageEntity:
    id: int
    title: Annotated[str, MinLen(1), MaxLen(100)]
    text: Annotated[str, MinLen(1)]


@dataclass
class FontColorEntity:
    id: int
    color: ColorFontEnum


@dataclass
class ServiceEntity:
    id: int
    name: Annotated[str, MinLen(1), MaxLen(100)]
    font_color: FontColorEntity
    image: str
    discount_message: Annotated[str, MaxLen(100)] = ""


@dataclass
class ServiceDetailEntity:
    id: int
    service: ServiceEntity
    quality_title: Annotated[str, MinLen(1), MaxLen(100)]
    quality_text: Annotated[str, MinLen(1)]
    advantage: list[AdvantageEntity] = field(default_factory=list)


@dataclass
class AboutBlockEntity:
    id: int
    first_title: Annotated[str, MinLen(1), MaxLen(100)]
    first_description: Annotated[str, MinLen(1)]
    second_title: Annotated[str, MinLen(1), MaxLen(100)]
    second_description: Annotated[str, MinLen(1)]


@dataclass
class AboutEntity:
    id: int
    title: Annotated[str, MinLen(1), MaxLen(100)]
    text: Annotated[str, MinLen(1)]
    blocks: list[AboutBlockEntity] = field(default_factory=list)


@dataclass
class ResultPhotoEntity:
    id: int
    image: str


@dataclass
class ResultEntity:
    id: int
    description: Annotated[str, MinLen(1)]
    result_photos: list[ResultPhotoEntity] = field(default_factory=list)


@dataclass
class FooterEntity:
    id: int
    email: Annotated[str, MinLen(3), MaxLen(254)]
    operating_mode: Annotated[str, MinLen(1), MaxLen(32)]
    address: Annotated[str, MinLen(1), MaxLen(64)]


@dataclass
class FAQEntity:
    id: int
    question: str
    answer: str


@dataclass
class SiteEntity:
    id: int
    whatsapp: Annotated[str, MinLen(1), MaxLen(256)]
    phone: Annotated[str, MinLen(1), MaxLen(32)]
    about: Optional[AboutEntity] = None
    results: Optional[ResultEntity] = None
    services: list[ServiceEntity] = field(default_factory=list)
    main_screen: Optional[MainScreenEntity] = None
    faq: list[FAQEntity] = field(default_factory=list)
    footer: Optional[FooterEntity] = None
