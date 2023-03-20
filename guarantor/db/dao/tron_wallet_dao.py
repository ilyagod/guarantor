from guarantor.db.dao.base import BaseDAO
from guarantor.db.models.tron_wallet import TronWallet


class TronWalletDAO(BaseDAO[TronWallet]):
    _model = TronWallet
