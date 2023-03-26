from loguru import logger
from tortoise.transactions import in_transaction

from guarantor.db.dao.deal_dao import DealDAO
from guarantor.db.dao.payment_dao import PaymentDAO
from guarantor.db.dao.user_correct_dao import UserCorrectDAO
from guarantor.enums import DealStatus
from guarantor.services.payment.payment_service import PaymentService
from guarantor.settings import settings


async def check_payments() -> None:
    payments = await PaymentDAO.get_payments_for_check()
    logger.info([x.id for x in payments])

    if settings.disable_check_payments:
        return

    if not payments:
        return

    svc = PaymentService()
    for payment in payments:
        if not await svc.check_status(payment.gateway.python_service, payment.id):
            continue
        # Success payment, create correct
        deals = await DealDAO.get_waiting_for_payment_deals(user_id=payment.user.id)
        if not deals:
            continue

        for deal in deals:
            balances = await UserCorrectDAO.get_balances_dict(deal.customer.id)
            if balances.get(deal.currency, 0) >= deal.price:
                async with in_transaction():
                    await UserCorrectDAO.create_correct(
                        deal.customer.id,
                        deal.price,
                        deal.currency,
                    )

                    deal.status = DealStatus.CONFIRM_PERFORMER
                    await deal.save()
