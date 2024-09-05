import json

from django.http import HttpRequest
from ninja import Router

from config.containers import get_container
from services.webhook.event_router import WebhookEventRouter
from .auth.handlers import router as auth_router
from .clients.handlers import router as client_router
from .landing.handlers import router as landing_router
from .jobs.handlers import router as jobs_router
from .schema import ResponseStatusSchema


router = Router(tags=["v1"])

router.add_router("landing", landing_router)
router.add_router("clients", auth_router)
router.add_router("clients", client_router)
router.add_router("crm", jobs_router)


@router.get(
    path="webhook/",
    response=ResponseStatusSchema,
    description="Получение вебхуков из CRM",
)
async def webhook(
    request: HttpRequest,
) -> ResponseStatusSchema:
    try:
        data = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return ResponseStatusSchema()
    container = get_container()
    webhook_router: WebhookEventRouter = container.resolve(WebhookEventRouter)
    await webhook_router.route_event(data)
    return ResponseStatusSchema()
