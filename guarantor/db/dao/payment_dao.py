from guarantor.db.dao.base import BaseDAO
from guarantor.db.models.payment import Payment


class PaymentDAO(BaseDAO[Payment]):
    _model = Payment
