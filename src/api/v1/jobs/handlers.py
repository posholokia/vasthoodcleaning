from django.http import HttpRequest
from ninja import Router
from loguru import logger

from api.v1.jobs.schema import JobSchema, JobDetailSchema
from apps.jobs.actions.job import JobAction
from apps.jobs.permissions import JobPermissions
from config.containers import get_container
from core.security.auth.jwt_auth import AuthBearer
from services.mapper import Mapper

router = Router(tags=["Jobs"])


@router.get(path="jobs/", response=list[JobSchema], auth=AuthBearer())
def get_jobs(
    request: HttpRequest
) -> list[JobSchema]:
    client_phone = request.auth  # type: ignore
    container = get_container()
    action: JobAction = container.resolve(JobAction)
    jobs = action.get_list(client_phone.lstrip("+1"))
    return [Mapper.dataclass_to_schema(JobSchema, job) for job in jobs]


@router.get(path="job/{job_id}/", response=JobDetailSchema, auth=AuthBearer())
def get_job_detail(
    job_id: str,
    request: HttpRequest
) -> JobDetailSchema:
    client_phone = request.auth  # type: ignore
    container = get_container()

    permission: JobPermissions = container.resolve(JobPermissions)
    permission.has_permission(client_phone, job_id)

    action: JobAction = container.resolve(JobAction)
    job = action.get_job_detail(job_id, client_phone)
    return Mapper.dataclass_to_schema(JobDetailSchema, job)
