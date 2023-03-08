from fastapi import APIRouter, Depends

from guarantor.db.models.user import User
from guarantor.services.user.user_service import UserService
from guarantor.web.api.v1.user.schema import (
    UserCreateOrUpdateSchema,
    UserResponseSchema,
)

router = APIRouter()


@router.post("/", response_model=UserResponseSchema)
async def create_or_update_user(
    data: UserCreateOrUpdateSchema,
    svc: UserService = Depends(UserService),
) -> User:
    """
    Create or update user
    """
    return await svc.create_or_update_user(data.name, data.external_id)
