import json

from django.http import HttpRequest
from loguru import logger
from ninja import Router

from services.webhook.event_router import WebhookEventRouter

from core.containers import get_container
from core.security.callable import crm_api_key_auth
from .auth.handlers import router as auth_router
from .jobs.handlers import router as jobs_router
from .landing.handlers import router as landing_router
from .schema import ResponseStatusSchema


router = Router(tags=["v1"])

router.add_router("landing", landing_router)
router.add_router("clients", auth_router)
router.add_router("crm", jobs_router)


@router.post(
    path="webhook/",
    response=ResponseStatusSchema,
    description="Получение вебхуков из CRM",
    auth=crm_api_key_auth(),
)
def webhook(
    request: HttpRequest,
) -> ResponseStatusSchema:
    try:
        data = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return ResponseStatusSchema()
    logger.warning("Webhook data: \n{}", data)
    container = get_container()
    webhook_router: WebhookEventRouter = container.resolve(WebhookEventRouter)
    webhook_router.route_event(data)
    return ResponseStatusSchema()
