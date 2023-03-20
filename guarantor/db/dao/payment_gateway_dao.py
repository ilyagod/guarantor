from guarantor.db.dao.base import BaseDAO
from guarantor.db.models.payment_gateway import PaymentGateway


class PaymentGatewayDAO(BaseDAO[PaymentGateway]):
    _model = PaymentGateway
