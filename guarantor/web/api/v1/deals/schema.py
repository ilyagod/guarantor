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
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[Currency] = None
    status: Optional[DealStatus] = None
    deadline_at: Optional[datetime.datetime] = None
    customer_id: Optional[int] = None
    performer_id: Optional[int] = None
