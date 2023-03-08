from enum import Enum


class Currency(str, Enum):
    RUB = "RUB"
    EUR = "EUR"
    USD = "USD"
    USDT = "USDT"


class DealStatus(str, Enum):
    CREATED = "created"
    DENY_PERFORMER = "deny_performer"
    CONFIRM_PERFORMER = "confirm_performer"
    IN_PROCESS = "in_process"
    CLOSE = "close"
    ARB_CLOSE_CUSTOMER = "arb_close_customer"
    ARB_CLOSE_PERFORMER = "arb_close_performer"


class DealType(str, Enum):
    COMMON = "common"


class DisputeStatus(str, Enum):
    OPEN = "open"
    CLOSED_SUCCESS = "closed_success"
    CLOSED_REJECTED = "closed_rejected"
