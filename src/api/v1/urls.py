from django.http import HttpRequest
from ninja import Router
from services.tasks_.tasks import webhook_handler

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
    webhook_handler.apply_async(args=(request.body,))
    return ResponseStatusSchema()
