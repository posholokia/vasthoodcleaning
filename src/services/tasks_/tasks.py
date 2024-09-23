import json

from apps.jobs.actions.job import JobAction
from celery import shared_task
from loguru import logger
from services.crm.http_request import HttpRequestError
from services.webhook.event_router import WebhookEventRouter

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


@shared_task(name="webhook_handler")
def webhook_handler(body: bytes) -> None:
    try:
        data = json.loads(body.decode())
    except json.JSONDecodeError:
        return
    logger.warning("Webhook data: \n{}", data)
    container = get_container()
    webhook_router: WebhookEventRouter = container.resolve(WebhookEventRouter)
    webhook_router.route_event(data)
