from fastapi import HTTPException

from guarantor.constants import (
    DEAL_CREATE_DISPUTE_ALLOWED,
    DISPUTE_UPDATE_STATUS_ALLOWED,
)


class BaseDealException(HTTPException):
    status_code: int = 400
    detail: str = "Error"

    def __init__(self) -> None:
        super().__init__(self.status_code, self.detail)


class DealNotFoundException(BaseDealException):
    status_code = 404
    detail = "Deal not found"


class DisputeCreateNotAllowed(BaseDealException):
    detail = f"Dispute can only be created for deals with statuses: {*(e.value for e in DEAL_CREATE_DISPUTE_ALLOWED), }"


class DisputeAlreadyCreated(BaseDealException):
    detail = "Dispute already created"


class DisputeDoesNotExists(BaseDealException):
    detail = "Dispute does not exists"


class DisputeUpdateNotAllowed(BaseDealException):
    detail = f"Dispute can only be updated in statuses: {*(e.value for e in DISPUTE_UPDATE_STATUS_ALLOWED), }"
