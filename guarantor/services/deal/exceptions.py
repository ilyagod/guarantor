from fastapi import HTTPException
from loguru import logger


class BaseDealException(HTTPException):
    status_code: int = 400
    detail: str = "Error"

    def __init__(self, detail: str = None) -> None:
        super().__init__(self.status_code, detail if detail else self.detail)


"""
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

"""


class CustomerUserNotFound(BaseDealException):
    detail = "Customer user not found"

    def __init__(self) -> None:
        logger.info("aaaa")
        super().__init__()


class PerformerUserNotFound(BaseDealException):
    detail = "Performer user not found"


class DealStatusChangeNotAllowed(BaseDealException):
    def __init__(self, from_status, to_status):
        super().__init__(f"Error change deal status from {from_status} to {to_status}")


class DisputeAlreadyCreated(BaseDealException):
    detail = "Dispute already created"


class DisputeCreateNotAllowed(BaseDealException):
    def __init__(self, deal_status):
        super().__init__(f"Error create dispute for deal with status {deal_status}")

class DisputeDoesNotExists(BaseDealException):
    detail = "Dispute does not exists"
