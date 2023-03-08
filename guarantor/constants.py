
from guarantor.enums import DealStatus

DEAL_UPDATE_STATUS_RULE = {
    DealStatus.CREATED: {DealStatus.DENY_PERFORMER, DealStatus.CONFIRM_PERFORMER},
    DealStatus.CONFIRM_PERFORMER: {DealStatus.CLOSE, DealStatus.ARB_CLOSE_PERFORMER, DealStatus.ARB_CLOSE_CUSTOMER}
}

DISPUTE_CREATE_STATUS_ALLOWED = {
    DealStatus.CONFIRM_PERFORMER,
}
