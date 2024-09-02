from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class JobStatus(Enum):
    unscheduled: str = "Unscheduled"
    scheduled: str = "Scheduled"
    in_progress: str = "In progress"
    completed: str = "Completed"
    canceled: str = "Canceled"


@dataclass
class ClientEntity:
    customer_ids: list[str]
    phone: str


@dataclass
class JobEntity:
    id: str
    schedule: datetime | None
    address: str
    status: JobStatus
    total_cost: int
