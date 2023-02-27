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
