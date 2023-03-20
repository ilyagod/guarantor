from fastapi import APIRouter

from guarantor.web.api.v1.deals.views import router as deals_router
from guarantor.web.api.v1.payment.views import router as payment_router
from guarantor.web.api.v1.user.views import router as user_router

v1_router = APIRouter()

v1_router.include_router(user_router, prefix="/user", tags=["Users"])
v1_router.include_router(deals_router, prefix="/deal", tags=["Deals"])
v1_router.include_router(payment_router, prefix="/payment", tags=["Payments"])
