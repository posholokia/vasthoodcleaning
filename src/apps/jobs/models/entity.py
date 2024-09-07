from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Union


T = Union[
    "SingleSelectEntity",
    "MultipleSelectEntity",
    "NumericalRangeEntity",
    "QuantitySelectEntity",
]


class JobStatus(str, Enum):
    unscheduled: str = "needs scheduling"
    scheduled: str = "scheduled"
    in_progress: str = "in progress"  # job.started
    completed: str = "complete unrated"  # job.completed
    canceled: str = "pro canceled"


@dataclass
class JobEntity:
    id: str
    schedule: datetime | None
    address: str
    status: JobStatus
    total_cost: int
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class MultipleSelectEntity:
    name: str
    choices: list[str]
    kind: str = field(init=False, default="multiple")


@dataclass
class NumericalRangeEntity:
    name: str
    choice: str
    kind: str = field(init=False, default="range")


@dataclass
class SingleSelectEntity:
    name: str
    choice: str
    kind: str = field(init=False, default="single")


@dataclass
class QuantitySelectEntity:
    name: str
    value: int
    kind: str = field(init=False, default="quantity")


class DiscountType(Enum):
    fixed: str = "fixed discount"
    percent: str = "percent discount"


@dataclass
class DiscountEntity:
    kind: DiscountType
    value: int


@dataclass
class DetailMaterialEntity:
    name: str
    quantity: float
    cost: int


@dataclass
class MaterialsEntity:
    total_cost: int
    detail: list[DetailMaterialEntity]


@dataclass
class JobPartEntity:
    name: str
    cost: int
    inlines: list[T] = field(default_factory=list)


@dataclass
class JobDetailEntity:
    parts: list[JobPartEntity]
    materials: MaterialsEntity | None = field(default=None)
    discount: DiscountEntity | None = field(default=None)




