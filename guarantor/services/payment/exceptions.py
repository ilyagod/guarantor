from typing import Optional

from fastapi import HTTPException


class BasePaymentException(HTTPException):
    status_code: int = 400
    detail: str = "Error"

    def __init__(self, detail: Optional[str] = None) -> None:
        super().__init__(self.status_code, detail if detail else self.detail)


class PaymentGatewayNotFound(BasePaymentException):
    detail = "Payment Gateway not found"
