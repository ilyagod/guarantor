from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from guarantor.db.models.payment_gateway import PaymentGateway
from guarantor.services.payment.payment_service import PaymentService
from guarantor.web.api.v1.payment.schema import (
    PaymentDepositRequest,
    PaymentDepositResponse,
    PaymentGatewayResponse,
    PaymentWithdrawRequest,
)

router = APIRouter()


@router.get("/gateways", response_model=List[PaymentGatewayResponse])
async def gateways_list(
    svc: PaymentService = Depends(),
) -> List[PaymentGateway]:
    """
    Payment Gateway List
    """
    return await svc.get_gateways()


@router.post("/deposit", response_model=PaymentDepositResponse)
async def deposit(
    data: PaymentDepositRequest,
    svc: PaymentService = Depends(),
) -> Dict[str, Any]:
    return await svc.create_payment(
        data.gateway_id,
        data.amount,
        data.user_id,
        data.currency,
    )


@router.post("/withdraw", response_model=PaymentDepositResponse)
async def withdraw(
    data: PaymentWithdrawRequest,
    svc: PaymentService = Depends(),
) -> Response:
    await svc.create_payment_withdraw(
        data.gateway_id,
        data.amount,
        data.user_id,
        data.currency,
        data.data,
    )

    return Response(status_code=status.HTTP_200_OK)
