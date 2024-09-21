from dataclasses import (
    dataclass,
    field,
)
from enum import Enum


class JobStatus(Enum):
    pending: str = "Pending"
    scheduled: str = "Scheduled"
    in_progress: str = "In Progress"
    completed: str = "Completed"
    canceled: str = "canceled"  # не отображается


class DiscountType(Enum):
    fixed: str = "fixed discount"
    percent: str = "percent discount"


@dataclass(frozen=True)
class DeleteTag:
    """
    По договоренности id тега захардкодили,
    чтобы не плодить теги и не тратить запросы в CRM.
    """

    id: str = field(init=False, default="tag_583f12bf1475460faa6b420cc167096c")
    name: str = field(init=False, default="deleted")
