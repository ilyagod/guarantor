from enum import Enum


class Currency(str, Enum):
    RUB = "RUB"
    EUR = "EUR"
    USD = "USD"


class DealStatus(str, Enum):
    UNCONFIRMED = "unconfirmed"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    DISPUTE_OPENED = "dispute_opened"
    COMPLETED_AFTER_DISPUTE = "completed_after_dispute"
    REJECTED_AFTER_DISPUTE = "rejected_after_dispute"


class DisputeStatus(str, Enum):
    OPEN = "open"
    CLOSED_SUCCESS = "closed_success"
    CLOSED_REJECTED = "closed_rejected"
