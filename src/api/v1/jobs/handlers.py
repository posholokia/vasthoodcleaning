from api.v1.jobs.schema import (
    JobDetailSchema,
    JobSchema,
)
from apps.jobs.actions.job import JobAction
from apps.jobs.permissions import JobPermissions
from django.http import HttpRequest
from ninja import Router

from core.containers import get_container
from core.mapper import dataclass_to_schema
from core.security.callable import client_jwt_auth


router = Router(tags=["Jobs"])


@router.get(
    path="jobs/",
    response=list[JobSchema],
    auth=client_jwt_auth(),
    description="List of all jobs for the current user",
)
def get_jobs(request: HttpRequest) -> list[JobSchema]:
    client_phone = request.auth  # type: ignore
    container = get_container()
    action: JobAction = container.resolve(JobAction)
    jobs = action.get_list(client_phone)
    return [dataclass_to_schema(JobSchema, job) for job in jobs]


@router.get(
    path="job/{job_id}/",
    response=JobDetailSchema,
    auth=client_jwt_auth(),
    description="Getting detailed information about the job.\n"
    "materials and discount can be null.",
)
def get_job_detail(request: HttpRequest, job_id: str) -> JobDetailSchema:
    client_phone = request.auth  # type: ignore
    container = get_container()

    permission: JobPermissions = container.resolve(JobPermissions)
    permission.has_permission(client_phone, job_id)

    action: JobAction = container.resolve(JobAction)
    job = action.get_job_detail(job_id, client_phone)
    return dataclass_to_schema(JobDetailSchema, job)
