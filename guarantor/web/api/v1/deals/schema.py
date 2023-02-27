import datetime
from typing import Optional

from pydantic import BaseModel

from guarantor.enums import Currency, DealStatus


class DealIncoming(BaseModel):
    """Схема входящего запроса для создания Deal"""

    title: str
    description: str
    price: float
    currency: Optional[Currency] = Currency.RUB
    deadline_at: Optional[datetime.datetime]


class DealOutgoing(BaseModel):
    """Схема ответа для Deal в апишку"""

    id: int
    title: str
    description: str
    price: float
    currency: Currency
    status: DealStatus
    deadline_at: Optional[datetime.datetime] = None
    created_at: datetime.datetime

    class Config:
        orm_mode = True
