from typing import Set

from guarantor.enums import DealStatus, DisputeStatus

DEAL_UPDATE_STATUS_ALLOWED: Set[DealStatus] = {
    DealStatus.UNCONFIRMED,
    DealStatus.CONFIRMED,
}

DEAL_CREATE_DISPUTE_ALLOWED: Set[DealStatus] = {
    DealStatus.CONFIRMED,
}


DISPUTE_UPDATE_STATUS_ALLOWED: Set[DisputeStatus] = {
    DisputeStatus.OPEN,
}

DISPUTE_TO_DEAL_STATUS_MAPPING = {
    DisputeStatus.CLOSED_SUCCESS: DealStatus.COMPLETED_AFTER_DISPUTE,
    DisputeStatus.CLOSED_REJECTED: DealStatus.REJECTED_AFTER_DISPUTE,
}
