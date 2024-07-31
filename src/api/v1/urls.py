from ninja import Router

from api.v1.landing.handlers import router as landing_router


router = Router(tags=["v1"])

router.add_router("landing", landing_router)
