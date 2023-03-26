from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from guarantor.db.models.deal import Deal
from guarantor.services.deal.deal_service import DealService
from guarantor.web.api.v1.deals.schema import (
    DealConfirmResponseSchema,
    DealCreateResponseSchema,
    DealCreateSchema,
    DisputeCreateSchema,
)

router = APIRouter()


@router.post("/", response_model=DealCreateResponseSchema)
async def create_deal(
    data: DealCreateSchema,
    svc: DealService = Depends(DealService),
) -> Deal:
    """
    Create Deal
    """
    return await svc.create_deal(**data.dict())


@router.get("/{deal_id}/confirm", response_model=DealConfirmResponseSchema)
async def confirm_deal(
    deal_id: int,
    svc: DealService = Depends(DealService),
) -> Deal:
    return await svc.confirm_deal(deal_id)


@router.get("/{deal_id}/deny")
async def deny_deal(
    deal_id: int,
    svc: DealService = Depends(DealService),
) -> Response:
    await svc.deny_deal(deal_id)
    return Response(status_code=status.HTTP_200_OK)


@router.post("/{deal_id}/dispute")
async def create_dispute(
    deal_id: int,
    data: DisputeCreateSchema,
    svc: DealService = Depends(DealService),
) -> Response:
    """
    Create Dispute
    """
    await svc.create_dispute(deal_id, data.title, data.description)
    return Response(status_code=status.HTTP_200_OK)


@router.get(
    "/{deal_id}/dispute/close_customer",
)
async def close_dispute_customer(
    deal_id: int,
    svc: DealService = Depends(DealService),
) -> Response:
    await svc.close_customer(deal_id)
    return Response(status_code=status.HTTP_200_OK)


@router.get(
    "/{deal_id}/dispute/close_performer",
)
async def close_dispute_performer(
    deal_id: int,
    svc: DealService = Depends(DealService),
) -> Response:
    await svc.close_performer(deal_id)
    return Response(status_code=status.HTTP_200_OK)


@router.get(
    "/{deal_id}/close",
)
async def close_deal(
    deal_id: int,
    svc: DealService = Depends(DealService),
) -> Response:
    await svc.close(deal_id)
    return Response(status_code=status.HTTP_200_OK)
