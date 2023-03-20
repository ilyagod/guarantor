from __future__ import annotations

import datetime
from typing import Optional

from pydantic import BaseModel

from guarantor.enums import Currency, DealType


class DealCreateSchema(BaseModel):
    """Create Deal Schema"""

    title: str
    description: str
    price: float
    currency: Optional[Currency] = Currency.RUB
    deadline_at: Optional[datetime.datetime]
    customer_id: int
    performer_id: int


class DealCreateResponseSchema(BaseModel):
    id: int
    deal_type: DealType


class DealConfirmResponseSchema(BaseModel):
    id: int


class DisputeCreateSchema(BaseModel):
    title: str
    description: str
