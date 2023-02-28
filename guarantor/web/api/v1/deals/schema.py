import datetime
from typing import Optional

from pydantic import BaseModel

from guarantor.enums import Currency, DealStatus


class DealCreateSchema(BaseModel):
    """Схема входящего запроса для создания Deal"""

    title: str
    description: str
    price: float
    currency: Optional[Currency] = Currency.RUB
    deadline_at: Optional[datetime.datetime]
    customer_id: int
    performer_id: int


class DealResponseSchema(BaseModel):
    """Схема ответа для Deal в апишку"""

    id: int
    title: str
    description: str
    price: float
    currency: Currency
    status: DealStatus
    deadline_at: Optional[datetime.datetime] = None
    created_at: datetime.datetime
    customer_id: int
    performer_id: int

    class Config:
        orm_mode = True


class DealUpdateSchema(BaseModel):
    title: str = None
    description: str = None
    price: float = None
    currency: Currency = None
    status: DealStatus = None
    deadline_at: datetime.datetime = None
    customer_id: int = None
    performer_id: int = None
