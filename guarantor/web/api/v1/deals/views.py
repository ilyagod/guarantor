from typing import List

from fastapi import APIRouter, Depends

from guarantor.db.models.deal import Deal
from guarantor.services.deal.deal_service import DealService
from guarantor.web.api.v1.deals.schema import (
    DealCreateSchema,
    DealResponseSchema,
    DealUpdateSchema,
    DisputeCreateSchema,
    DisputeUpdateSchema,
)

router = APIRouter()


@router.get("/", response_model=List[DealResponseSchema])
async def list_deals(
    svc: DealService = Depends(DealService),
) -> List[Deal]:
    """
    List Deal
    """
    return await svc.get_all_deals()


@router.post("/", response_model=DealResponseSchema)
async def create_deal(
    deal: DealCreateSchema,
    svc: DealService = Depends(DealService),
) -> Deal:
    """
    Create Deal
    """
    return await svc.create_deal(deal.dict(exclude_none=True))


@router.get("/{deal_id}", response_model=DealResponseSchema)
async def get_deal(svc: DealService = Depends(DealService)) -> Deal:
    """
    Get Deal
    """
    return await svc.get_deal()


@router.patch("/{deal_id}", response_model=DealResponseSchema)
async def update_deal(
    data: DealUpdateSchema,
    svc: DealService = Depends(DealService),
) -> Deal:
    """
    Partial update Deal
    """
    return await svc.update_deal(data.dict(exclude_none=True))


@router.post("/{deal_id}/dispute", response_model=DealResponseSchema)
async def create_dispute(
    data: DisputeCreateSchema,
    svc: DealService = Depends(DealService),
) -> Deal:
    """
    Create Dispute
    """
    return await svc.create_dispute(data.dict(exclude_none=True))


@router.patch("/{deal_id}/dispute", response_model=DealResponseSchema)
async def update_dispute(
    data: DisputeUpdateSchema,
    svc: DealService = Depends(DealService),
) -> Deal:
    """
    Partial update Dispute
    """
    return await svc.update_dispute(data.dict(exclude_none=True))
