from guarantor.db.dao.base import BaseDAO
from guarantor.db.models.deal import Deal


class DealDAO(BaseDAO):
    _model = Deal
