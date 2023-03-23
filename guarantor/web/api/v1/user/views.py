from typing import Any, Dict, List

from fastapi import APIRouter, Depends

from guarantor.db.dao.user_correct_dao import UserCorrectDAO
from guarantor.db.models.user import User
from guarantor.services.user.user_service import UserService
from guarantor.web.api.v1.user.schema import (
    UserBalanceResponseSchema,
    UserCreateOrUpdateResponseSchema,
    UserCreateOrUpdateSchema,
)

router = APIRouter()


@router.post("/", response_model=UserCreateOrUpdateResponseSchema)
async def create_or_update_user(
    data: UserCreateOrUpdateSchema,
    svc: UserService = Depends(UserService),
) -> User:
    """
    Create or update user
    """
    return await svc.create_or_update_user(data.name, data.external_id)


@router.get("/{user_id}/balance", response_model=List[UserBalanceResponseSchema])
async def user_balance(
    user_id: int,
) -> List[Dict[str, Any]]:
    """
    User Balance
    """
    return await UserCorrectDAO.get_balances(user_id)
