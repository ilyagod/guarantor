from loguru import logger

from guarantor.db.dao.payment_dao import PaymentDAO
from guarantor.services.payment.payment_service import PaymentService


async def check_payments() -> None:
    payments = await PaymentDAO.get_payments_for_check()
    logger.info([x.id for x in payments])
    return
    if not payments:
        return

    svc = PaymentService()
    for payment in payments:
        await svc.check_status(payment.gateway.python_module, payment.id)
