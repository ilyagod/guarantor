import importlib
from typing import Any, Dict, List, Union

from tortoise.transactions import atomic, in_transaction

from guarantor.db.dao.payment_dao import PaymentDAO
from guarantor.db.dao.payment_gateway_dao import PaymentGatewayDAO
from guarantor.db.dao.user_correct_dao import UserCorrectDAO
from guarantor.db.models.payment_gateway import PaymentGateway
from guarantor.enums import Currency
from guarantor.services.payment.exceptions import (
    PaymentGatewayNotFound,
    WithdrawPaymentAmountMoreBalance,
)
from guarantor.services.tron.tron_service import TronService


class PaymentService:
    @atomic()
    async def create_payment(
        self,
        gateway_id: int,
        amount: float,
        user_id: int,
        currency: Currency,
    ) -> Dict[str, Any]:
        payment_gateway = await PaymentGatewayDAO.get_or_none({"id": gateway_id})
        if not payment_gateway:
            raise PaymentGatewayNotFound

        payment = await PaymentDAO.create(
            {
                "gateway_id": gateway_id,
                "amount": amount,
                "user_id": user_id,
                "currency": currency,
            },
        )

        svc = self.get_gateway_module(payment_gateway.python_service)
        gateway_data = await svc.create_payment(
            gateway_id,
            amount,
            user_id,
            currency,
            payment.id,
        )

        return {
            "amount": payment.amount,
            "currency": payment.currency,
            "status": payment.status,
            "gateway_data": gateway_data,
        }

    async def create_payment_withdraw(
        self,
        gateway_id: int,
        amount: float,
        user_id: int,
        currency: Currency,
        data: Dict[str, Any],
    ) -> None:
        payment_gateway = await PaymentGatewayDAO.get_or_none({"id": gateway_id})
        if not payment_gateway:
            raise PaymentGatewayNotFound

        balances = await UserCorrectDAO.get_balances_dict(user_id)
        if balances.get(currency, 0) < amount:
            raise WithdrawPaymentAmountMoreBalance

        async with in_transaction():
            await UserCorrectDAO.create_correct(user_id, amount * -1, currency)

            payment = await PaymentDAO.create(
                {
                    "gateway_id": gateway_id,
                    "amount": amount * -1,
                    "user_id": user_id,
                    "currency": currency,
                    "withdraw": True,
                    "data": data,
                },
            )

            svc = self.get_gateway_module(payment_gateway.python_service)
            await svc.create_payment_withdraw(
                gateway_id,
                amount,
                user_id,
                currency,
                payment.id,
                data,
            )

    async def get_gateways(self) -> List[PaymentGateway]:
        return await PaymentGatewayDAO.all()

    @classmethod
    def get_gateway_module(cls, name: str) -> Union[TronService]:
        svc = importlib.import_module(f"guarantor.services.{name}.{name}_service")
        return getattr(svc, f"{name.title()}Service")()

    @classmethod
    async def check_status(cls, python_service: str, payment_id: int) -> bool:
        svc = cls.get_gateway_module(python_service)
        return await svc.check_status(payment_id)
