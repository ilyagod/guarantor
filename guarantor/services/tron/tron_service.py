from typing import Any, Dict

import httpx
from tortoise.transactions import in_transaction
from tronpy import AsyncTron

from guarantor.db.dao.payment_dao import PaymentDAO
from guarantor.db.dao.tron_wallet_dao import TronWalletDAO
from guarantor.db.dao.user_correct_dao import UserCorrectDAO
from guarantor.db.dao.user_dao import UserDAO
from guarantor.enums import Currency, PaymentStatus
from guarantor.settings import settings


class TronService:
    # def __init__(self):
    #    #self.client = Tron(network=settings.payments_tron_network)

    @classmethod
    async def generate_address(cls) -> Dict[str, Any]:
        async with AsyncTron(network=settings.payments_tron_network) as client:
            return client.generate_address()

    #  async def calculate_need_energy(self):

    async def create_payment_withdraw(
        self,
        gateway_id: int,
        amount: float,
        user_id: int,
        currency: Currency,
        payment_id: int,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        result = await self.transfer(
            settings.payments_tron_main_wallet_config["base58check_address"],
            settings.payments_tron_main_wallet_config["hex_address"],
            data.get("wallet", ""),
            amount,
        )
        await PaymentDAO.update(payment_id, {"status": PaymentStatus.SUCCESS})
        return result

    async def create_payment(
        self,
        gateway_id: int,
        amount: float,
        user_id: int,
        currency: Currency,
        payment_id: int,
    ) -> Dict[str, Any]:
        user = await UserDAO.get_by_id(user_id)
        wallet = user.tron_wallet
        if not user.tron_wallet:
            new_wallet = await self.generate_address()
            wallet = await TronWalletDAO.create(
                {
                    "address": new_wallet["base58check_address"],
                    "private_key": new_wallet["private_key"],
                    "public_key": new_wallet["public_key"],
                },
            )
            await user.refresh_from_db()
        return {"address": wallet.address}

    async def get_balance(self, address: str, token_type: str = "usdt") -> float:
        subdomain = (
            f"{settings.payments_tron_network}api"
            if settings.payments_tron_network != "mainnet"
            else "api"
        )
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://{subdomain}.tronscan.org/api/account/tokens"
                f"?address={address}",
            )
            for token in r.json()["data"]:
                if token["tokenAbbr"].lower() == token_type.lower():
                    return token["quantity"]
        return 0

    async def check_status(self, payment_id: int) -> bool:
        wallet = await TronWalletDAO.get_or_none({"payment_id": payment_id})
        payment = await PaymentDAO.get_by_id(payment_id)
        if not wallet:
            return False
        balance = await self.get_balance(wallet.address)

        if payment.amount != balance:
            return False

        async with in_transaction():
            await self.trx_transfer(
                settings.payments_tron_main_wallet_config["base58check_address"],
                settings.payments_tron_main_wallet_config["private_key"],
                wallet.address,
                settings.payments_tron_trx_commission,
            )
            await self.transfer(
                wallet.address,
                wallet.private_key,
                settings.payments_tron_main_wallet_config["base58check_address"],
                balance,
            )

            payment.status = PaymentStatus.SUCCESS
            await payment.save()

            await UserCorrectDAO.create_correct(payment.user.id, balance, Currency.USDT)

            return True

    async def transfer(
        self,
        from_address: str,
        from_private_key: str,
        to_address: str,
        amount: float,
    ) -> dict[str, Any]:
        async with AsyncTron(network=settings.payments_tron_network) as client:
            contract = await client.get_contract(
                settings.payments_tron_usdt_trc20_address,
            )
            txb = (
                contract.functions.transfer(to_address, amount)
                .with_owner(from_address)
                .fee_limit(settings.payments_tron_fee_limit)
            )
            txn = await txb.build()
            txn_ret = await txn.sign(from_private_key).broadcast()
            return await txn_ret.wait()

    async def trx_transfer(
        self,
        from_address: str,
        from_private_key: str,
        to_address: str,
        amount: float,
    ) -> dict[str, Any]:
        async with AsyncTron(network=settings.payments_tron_network) as client:
            txb = client.trx.transfer(
                from_address,
                to_address,
                amount,
            ).memo("test memo")
            txn = await txb.build()
            txn_ret = await txn.sign(from_private_key)
            return await txn_ret.wait()
