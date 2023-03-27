from __future__ import annotations

import datetime
from typing import Optional

from pydantic import BaseModel

from guarantor.enums import Currency, DealType


class DealCreateSchema(BaseModel):
    """Create Deal schema"""

    title: str
    description: str
    price: float
    currency: Optional[Currency] = Currency.USDT
    deadline_at: Optional[datetime.datetime]
    customer_id: int
    performer_id: int


class DealCreateResponseSchema(BaseModel):
    """Response schema after create Deal"""

    id: int
    deal_type: DealType


class DealConfirmResponseSchema(BaseModel):
    """Response schema after confirm deal"""

    id: int


class DisputeCreateSchema(BaseModel):
    """Create dispute schema"""

    title: str
    description: str
