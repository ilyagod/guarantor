from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from guarantor.enums import Currency, PaymentStatus


class PaymentGatewayResponse(BaseModel):
    id: int
    name: str
    logo: Optional[str] = None
    currency: List[Currency]


class PaymentDepositRequest(BaseModel):
    gateway_id: int
    amount: float
    user_id: int
    currency: Currency


class PaymentDepositResponse(BaseModel):
    amount: float
    currency: Currency
    status: PaymentStatus
    gateway_data: Optional[Dict[str, Any]] = {}
