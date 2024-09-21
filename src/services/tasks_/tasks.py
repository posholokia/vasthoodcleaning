from apps.jobs.actions.job import JobAction
from celery import shared_task
from loguru import logger
from services.crm.http_request import HttpRequestError

from core.containers import get_container


@shared_task(name="cancel_job_task")
def cancel_job_task(job_id: str) -> None:
    logger.debug("Запущена задача на отмену работы {}", job_id)
    container = get_container()
    action: JobAction = container.resolve(JobAction)
    try:
        action.cancel_job(job_id)
    except HttpRequestError:
        cancel_job_task.apply_async(args=(job_id,), countdown=30)
