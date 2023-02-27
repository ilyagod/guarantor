from fastapi.routing import APIRouter

from guarantor.web.api import monitoring
from guarantor.web.api.v1.router import v1_router

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(v1_router, prefix="/v1")
