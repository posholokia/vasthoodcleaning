from ninja import Router

from .auth.handlers import router as auth_router
from .clients.handlers import router as client_router
from .landing.handlers import router as landing_router


router = Router(tags=["v1"])

router.add_router("landing", landing_router)
router.add_router("clients", auth_router)
router.add_router("clients", client_router)
