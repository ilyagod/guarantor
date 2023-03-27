from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from guarantor.enums import Currency, PaymentStatus


class PaymentGatewayResponse(BaseModel):
    """Response schema for payment gateways"""

    id: int
    name: str
    logo: Optional[str] = None
    currency: List[Currency]


class PaymentDepositRequest(BaseModel):
    """Deposit payment schema"""

    gateway_id: int
    amount: float
    user_id: int
    currency: Currency


class PaymentDepositResponse(BaseModel):
    """Response schema after deposit"""

    amount: float
    currency: Currency
    status: PaymentStatus
    gateway_data: Optional[Dict[str, Any]] = {}


class PaymentWithdrawRequest(BaseModel):
    gateway_id: int
    amount: float
    user_id: int
    currency: Currency
    data: Dict[str, Any]
