from datetime import datetime
from typing import Any

from apps.jobs.models import (
    DeleteTag,
    JobEntity,
    JobStatus,
)


JobCrmStatus = {
    "needs scheduling": JobStatus.pending,
    "scheduled": JobStatus.scheduled,
    "in progress": JobStatus.in_progress,
    "complete unrated": JobStatus.completed,
    "complete rated": JobStatus.completed,
    "pro canceled": JobStatus.canceled,
    "user canceled": JobStatus.canceled,
}


def parse_job(job_data: dict[str, Any]) -> JobEntity:
    """
    Парсинг работы.

    :param job_data:    Json из crm с данными о работе.
    :return:            Работа.
    """
    date_format = "%Y-%m-%dT%H:%M:%S%z"
    schedule: str | None = job_data["schedule"]["scheduled_start"]

    if schedule is not None:
        schedule: datetime = datetime.strptime(schedule, date_format)
    last_updated_str: str = job_data["updated_at"]
    last_updated: datetime = datetime.strptime(last_updated_str, date_format)

    job_id: str = job_data["id"]
    address: str = _get_address_string(job_data["address"])
    status = JobCrmStatus.get(job_data["work_status"])
    total_cost: int = job_data["total_amount"]
    paid: bool = not job_data["outstanding_balance"]

    tags: list[str] = job_data["tags"]
    if DeleteTag.name in tags:
        status = JobStatus.canceled

    return JobEntity(
        id=job_id,
        schedule=schedule,
        address=address,
        status=status,
        total_cost=total_cost,
        paid=paid,
        last_updated=last_updated,
    )


def _get_address_string(address_dict: dict) -> str:
    """
    Вспомогательный метод для конвертации адреса из словаря в строку.

    :param address_dict:    Json с адресом.
    :return:                Адрес.
    """
    street: str = address_dict["street"]
    street_line_2: str = address_dict["street_line_2"]
    city: str = address_dict["city"]
    state: str = address_dict["state"]
    return f"{street} {street_line_2} {city} {state}"


if __name__ == "__main__":
    "tag_583f12bf1475460faa6b420cc167096c"

    job_updated = {
        "event": "job.updated",
        "company_id": "d3514589-8266-4fcf-aa56-af658b20f8ab",
        "job": {
            "id": "job_3aa4a67ffd77424fa78aeca4e9ca6557",
            "invoice_number": "29",
            "description": "House Cleaning",
            "customer": {
                "id": "cus_f72ace0117244beb85fe7175b9131de3",
                "first_name": "Arkadii",
                "last_name": "Astvatsaturov",
                "email": "arkady017@gmail.com",
                "mobile_number": "7639103848",
                "home_number": None,
                "work_number": None,
                "company": None,
                "notifications_enabled": True,
                "lead_source": None,
                "notes": None,
                "created_at": "2024-09-06T02:19:46Z",
                "updated_at": "2024-09-06T02:19:46Z",
                "company_name": "VAST CLEANING",
                "company_id": "d3514589-8266-4fcf-aa56-af658b20f8ab",
                "tags": [],
            },
            "address": {
                "id": "adr_00950059aad0470a970995cd104f3627",
                "type": "service",
                "street": "4932 Acacia St",
                "street_line_2": "",
                "city": "San Gabriel",
                "state": "CA",
                "zip": "91776",
                "country": "US",
            },
            "notes": [
                {
                    "id": "nte_6eb40837f2f1456691fb24dd8c87062f",
                    "content": "House Cleaning:\\nDescription:\\n- no description provided",
                }
            ],
            "work_status": "scheduled",
            "work_timestamps": {
                "on_my_way_at": None,
                "started_at": None,
                "completed_at": None,
            },
            "schedule": {
                "scheduled_start": "2024-09-09T07:00:00Z",
                "scheduled_end": "2024-09-09T07:00:00Z",
                "arrival_window": 0,
                "appointments": [],
            },
            "total_amount": 14900,
            "outstanding_balance": 14900,
            "assigned_employees": [
                {
                    "id": "pro_d732eca4f2804f588828b9b5522973ab",
                    "first_name": "Arkadii",
                    "last_name": "Astvatsaturov",
                    "email": "arkady017@gmail.com",
                    "mobile_number": "7639103848",
                    "color_hex": "EF9159",
                    "avatar_url": "/assets/add_image_thumb.png",
                    "role": "field tech",
                    "tags": [],
                    "permissions": {
                        "can_add_and_edit_job": True,
                        "can_be_booked_online": True,
                        "can_call_and_text_with_customers": True,
                        "can_chat_with_customers": True,
                        "can_delete_and_cancel_job": True,
                        "can_edit_message_on_invoice": True,
                        "can_see_street_view_data": True,
                        "can_share_job": False,
                        "can_take_payment_see_prices": True,
                        "can_see_customers": True,
                        "can_see_full_schedule": True,
                        "can_see_future_jobs": True,
                        "can_see_marketing_campaigns": True,
                        "can_see_reporting": True,
                        "can_edit_settings": True,
                        "is_point_of_contact": False,
                        "is_admin": True,
                    },
                    "company_name": "VAST CLEANING",
                    "company_id": "d3514589-8266-4fcf-aa56-af658b20f8ab",
                }
            ],
            "tags": [],
            "original_estimate_id": None,
            "original_estimate_uuids": [],
            "lead_source": "Online Booking",
            "job_fields": {"job_type": None, "business_unit": None},
            "created_at": "2024-09-06T02:19:46Z",
            "updated_at": "2024-09-06T02:19:47Z",
            "company_name": "VAST CLEANING",
            "company_id": "d3514589-8266-4fcf-aa56-af658b20f8ab",
            "attachments": [],
        },
    }

    job_created = {
        "event": "job.created",
        "company_id": "d3514589-8266-4fcf-aa56-af658b20f8ab",
        "job": {
            "id": "job_3aa4a67ffd77424fa78aeca4e9ca6557",
            "invoice_number": "29",
            "description": "House Cleaning",
            "customer": {
                "id": "cus_f72ace0117244beb85fe7175b9131de3",
                "first_name": "Arkadii",
                "last_name": "Astvatsaturov",
                "email": "arkady017@gmail.com",
                "mobile_number": "7639103848",
                "home_number": None,
                "work_number": None,
                "company": None,
                "notifications_enabled": True,
                "lead_source": None,
                "notes": None,
                "created_at": "2024-09-06T02:19:46Z",
                "updated_at": "2024-09-06T02:19:46Z",
                "company_name": "VAST CLEANING",
                "company_id": "d3514589-8266-4fcf-aa56-af658b20f8ab",
                "tags": [],
            },
            "address": {
                "id": "adr_00950059aad0470a970995cd104f3627",
                "type": "service",
                "street": "4932 Acacia St",
                "street_line_2": "",
                "city": "San Gabriel",
                "state": "CA",
                "zip": "91776",
                "country": "US",
            },
            "notes": [
                {
                    "id": "nte_6eb40837f2f1456691fb24dd8c87062f",
                    "content": "House Cleaning:\\nDescription:\\n- no description provided",
                }
            ],
            "work_status": "scheduled",
            "work_timestamps": {
                "on_my_way_at": None,
                "started_at": None,
                "completed_at": None,
            },
            "schedule": {
                "scheduled_start": "2024-09-09T07:00:00Z",
                "scheduled_end": "2024-09-09T07:00:00Z",
                "arrival_window": 0,
                "appointments": [],
            },
            "total_amount": 14900,
            "outstanding_balance": 14900,
            "assigned_employees": [
                {
                    "id": "pro_d732eca4f2804f588828b9b5522973ab",
                    "first_name": "Arkadii",
                    "last_name": "Astvatsaturov",
                    "email": "arkady017@gmail.com",
                    "mobile_number": "7639103848",
                    "color_hex": "EF9159",
                    "avatar_url": "/assets/add_image_thumb.png",
                    "role": "field tech",
                    "tags": [],
                    "permissions": {
                        "can_add_and_edit_job": True,
                        "can_be_booked_online": True,
                        "can_call_and_text_with_customers": True,
                        "can_chat_with_customers": True,
                        "can_delete_and_cancel_job": True,
                        "can_edit_message_on_invoice": True,
                        "can_see_street_view_data": True,
                        "can_share_job": False,
                        "can_take_payment_see_prices": True,
                        "can_see_customers": True,
                        "can_see_full_schedule": True,
                        "can_see_future_jobs": True,
                        "can_see_marketing_campaigns": True,
                        "can_see_reporting": True,
                        "can_edit_settings": True,
                        "is_point_of_contact": False,
                        "is_admin": True,
                    },
                    "company_name": "VAST CLEANING",
                    "company_id": "d3514589-8266-4fcf-aa56-af658b20f8ab",
                }
            ],
            "tags": [],
            "original_estimate_id": None,
            "original_estimate_uuids": [],
            "lead_source": "Online Booking",
            "job_fields": {"job_type": None, "business_unit": None},
            "created_at": "2024-09-06T02:19:46Z",
            "updated_at": "2024-09-06T02:19:47Z",
            "company_name": "VAST CLEANING",
            "company_id": "d3514589-8266-4fcf-aa56-af658b20f8ab",
            "attachments": [],
        },
    }
    parse_job(job_updated["job"])
