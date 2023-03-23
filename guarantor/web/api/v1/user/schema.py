from pydantic import BaseModel

from guarantor.enums import Currency


class UserCreateOrUpdateSchema(BaseModel):
    """Create or update user schema"""

    name: str
    external_id: int


class UserCreateOrUpdateResponseSchema(BaseModel):
    """Response schema after create user"""

    id: int


class UserBalanceResponseSchema(BaseModel):
    """Response schema for user balance"""

    currency: Currency
    balance: float
