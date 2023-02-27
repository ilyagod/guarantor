from fastapi import APIRouter

from guarantor.web.api.v1.deals.views import router as deals_router

v1_router = APIRouter()


v1_router.include_router(deals_router, prefix="/deals")
