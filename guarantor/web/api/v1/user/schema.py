from pydantic import BaseModel

from guarantor.enums import Currency


class UserCreateOrUpdateSchema(BaseModel):
    name: str
    external_id: int


class UserCreateOrUpdateResponseSchema(BaseModel):
    id: int


class UserBalanceResponseSchema(BaseModel):
    currency: Currency
    balance: float
