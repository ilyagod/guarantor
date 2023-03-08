
from fastapi import APIRouter, Depends

from guarantor.db.models.deal import Deal
from guarantor.services.deal.deal_service import DealService
from guarantor.web.api.v1.deals.schema import (  # DealResponseSchema,; DealUpdateSchema,; DisputeCreateSchema,; DisputeUpdateSchema,
    DealCreateResponseSchema,
    DealCreateSchema,
    DealFullResponseSchema,
    DisputeCreateSchema,
)

router = APIRouter()

'''
@router.get("/", response_model=List[DealResponseSchema])
async def list_deals(
    svc: DealService = Depends(DealService),
) -> List[Deal]:
    """
    List Deal
    """
    return await svc.get_all_deals()
'''


@router.post("/", response_model=DealCreateResponseSchema)
async def create_deal(
    data: DealCreateSchema,
    svc: DealService = Depends(DealService),
) -> Deal:
    """
    Create Deal
    """
    return await svc.create_deal(
        data.title,
        data.description,
        data.price,
        data.currency,
        data.customer_id,
        data.performer_id,
        data.deadline_at,
    )


@router.get("/{deal_id}/confirm", response_model=DealCreateResponseSchema)
async def confirm_deal(
    deal_id: int,
    svc: DealService = Depends(DealService),
):
    return await svc.confirm_deal(deal_id)


@router.get("/{deal_id}/deny", response_model=DealCreateResponseSchema)
async def deny_deal(
    deal_id: int,
    svc: DealService = Depends(DealService),
):
    return await svc.deny_deal(deal_id)


@router.post("/{deal_id}/dispute", response_model=DealFullResponseSchema)
async def create_dispute(
    deal_id: int,
    data: DisputeCreateSchema,
    svc: DealService = Depends(DealService),
) -> Deal:
    """
    Create Dispute
    """
    return await svc.create_dispute(deal_id, data.title, data.description)


@router.get("/{deal_id}/dispute/close_customer", response_model=DealCreateResponseSchema)
async def deny_deal(
    deal_id: int,
    svc: DealService = Depends(DealService),
):
    return await svc.close_customer(deal_id)


@router.get("/{deal_id}/dispute/close_performer", response_model=DealCreateResponseSchema)
async def deny_deal(
    deal_id: int,
    svc: DealService = Depends(DealService),
):
    return await svc.close_performer(deal_id)


'''
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
'''
