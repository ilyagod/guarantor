from guarantor.db.dao.base import BaseDAO
from guarantor.db.models.dispute import Dispute


class DisputeDAO(BaseDAO):
    _model = Dispute
