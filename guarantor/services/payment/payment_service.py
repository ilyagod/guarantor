import importlib

from tortoise.transactions import atomic

from guarantor.db.dao.payment_dao import PaymentDAO
from guarantor.db.dao.payment_gateway_dao import PaymentGatewayDAO
from guarantor.enums import Currency
from guarantor.services.payment.exceptions import PaymentGatewayNotFound


class PaymentService:
    @atomic()
    async def create_payment(
        self, gateway_id: int, amount: float, user_id: int, currency: Currency
    ):
        payment_gateway = await PaymentGatewayDAO.get_or_none({"id": gateway_id})
        if not payment_gateway:
            raise PaymentGatewayNotFound

        payment = await PaymentDAO.create(
            {
                "gateway_id": gateway_id,
                "amount": amount,
                "user_id": user_id,
                "currency": currency,
            }
        )

        svc = self._get_gateway(payment_gateway.python_service)
        gateway_data = await svc.create_payment(
            gateway_id, amount, user_id, currency, payment.id
        )

        return {
            "amount": payment.amount,
            "currency": payment.currency,
            "status": payment.status,
            "gateway_data": gateway_data,
        }

    def get_gateways(self):
        return PaymentGatewayDAO.get_all(100, 0)

    def _get_gateway(self, name):
        svc = importlib.import_module(f"guarantor.services.{name}.{name}_service")
        return getattr(svc, f"{name.title()}Service")()
