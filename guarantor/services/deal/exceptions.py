from typing import Optional

from fastapi import HTTPException

from guarantor.enums import DealStatus


class BaseDealException(HTTPException):
    status_code: int = 400
    detail: str = "Error"

    def __init__(self, detail: Optional[str] = None) -> None:
        super().__init__(self.status_code, detail if detail else self.detail)


class CustomerUserNotFound(BaseDealException):
    detail = "Customer user not found"


class PerformerUserNotFound(BaseDealException):
    detail = "Performer user not found"


class DealStatusChangeNotAllowed(BaseDealException):
    def __init__(self, from_status: DealStatus, to_status: DealStatus):
        super().__init__(f"Error change deal status from {from_status} to {to_status}")


class DisputeAlreadyCreated(BaseDealException):
    detail = "Dispute already created"


class DisputeCreateNotAllowed(BaseDealException):
    def __init__(self, deal_status: DealStatus) -> None:
        super().__init__(f"Error create dispute for deal with status {deal_status}")


class DisputeDoesNotExists(BaseDealException):
    detail = "Dispute does not exists"
