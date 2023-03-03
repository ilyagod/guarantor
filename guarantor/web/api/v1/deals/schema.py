import datetime
from typing import Optional

from pydantic import BaseModel

from guarantor.enums import Currency, DealStatus, DisputeStatus


class DisputeCreateSchema(BaseModel):
    """Схема создания спора"""

    title: str
    description: str


class DisputeResponseSchema(BaseModel):
    """Схема ответа для спора внутри сделки"""
    title: str
    description: str
    status: DisputeStatus


class DisputeUpdateSchema(BaseModel):
    """Схема обновления спора"""
    title: Optional[str]
    description: Optional[str]
    status: Optional[DisputeStatus]


class DealCreateSchema(BaseModel):
    """Схема запроса для создания сделки"""

    title: str
    description: str
    price: float
    currency: Optional[Currency] = Currency.RUB
    deadline_at: Optional[datetime.datetime]
    customer_id: int
    performer_id: int


class DealResponseSchema(BaseModel):
    """Схема ответа для сделки"""

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
    dispute: Optional[DisputeResponseSchema] = None

    class Config:
        orm_mode = True


class DealUpdateSchema(BaseModel):
    """Схема обновления сделки"""

    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[Currency] = None
    status: Optional[DealStatus] = None
    deadline_at: Optional[datetime.datetime] = None
    customer_id: Optional[int] = None
    performer_id: Optional[int] = None

