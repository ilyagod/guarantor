from enum import Enum


class Currency(str, Enum):
    RUB = "RUB"
    EUR = "EUR"
    USD = "USD"
    USDT = "USDT"


class DealStatus(str, Enum):
    CREATED = "created"
    DENY_PERFORMER = "deny_performer"
    WAITING_FOR_PAYMENT = "waiting_for_payment"
    CONFIRM_PERFORMER = "confirm_performer"
    CLOSE = "close"
    ARB_CLOSE_CUSTOMER = "arb_close_customer"
    ARB_CLOSE_PERFORMER = "arb_close_performer"


class DealType(str, Enum):
    COMMON = "common"


class PaymentStatus(str, Enum):
    WAITING = "waiting"
    SUCCESS = "success"
    ERROR = "error"


class TronWalletStatus(str, Enum):
    WAITING = "waiting"
    RECEIVED = "received"
    TRANSFERED = "transfered"
