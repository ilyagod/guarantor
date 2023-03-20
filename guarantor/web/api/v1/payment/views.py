from typing import List

from fastapi import APIRouter, Depends

from guarantor.services.payment.payment_service import PaymentService
from guarantor.web.api.v1.payment.schema import (
    PaymentDepositRequest,
    PaymentDepositResponse,
    PaymentGatewayResponse,
)

router = APIRouter()


@router.get("/gateways", response_model=List[PaymentGatewayResponse])
async def gateways_list(
    svc: PaymentService = Depends(),
) -> dict:
    """
    Payment Gateway List
    """
    return await svc.get_gateways()


@router.post("/deposit", response_model=PaymentDepositResponse)
async def deposit(
    data: PaymentDepositRequest,
    svc: PaymentService = Depends(),
):
    return await svc.create_payment(
        data.gateway_id, data.amount, data.user_id, data.currency
    )
