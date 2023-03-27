from typing import Any, Dict

import httpx
from tortoise.transactions import in_transaction
from tronpy import AsyncTron

from guarantor.db.dao.payment_dao import PaymentDAO
from guarantor.db.dao.tron_wallet_dao import TronWalletDAO
from guarantor.db.dao.user_correct_dao import UserCorrectDAO
from guarantor.enums import Currency, PaymentStatus, TronWalletStatus
from guarantor.settings import settings


class TronService:
    # def __init__(self):
    #    #self.client = Tron(network=settings.tron_network)

    @classmethod
    async def generate_address(cls) -> Dict[str, Any]:
        async with AsyncTron(network=settings.tron_network) as client:
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
            settings.main_wallet_config["base58check_address"],
            settings.main_wallet_config["hex_address"],
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
        wallet = await self.generate_address()
        await TronWalletDAO.create(
            {
                "address": wallet["base58check_address"],
                "private_key": wallet["private_key"],
                "public_key": wallet["public_key"],
                "amount": amount,
                "payment_id": payment_id,
            },
        )
        return {"address": wallet["base58check_address"]}

    async def get_balance(self, address: str, token_type: str = "usdt") -> float:
        subdomain = (
            f"{settings.tron_network}api"
            if settings.tron_network != "mainnet"
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

        if wallet.amount != balance:
            return False

        async with in_transaction():
            await self.trx_transfer(
                settings.main_wallet_config["base58check_address"],
                settings.main_wallet_config["private_key"],
                wallet.address,
                settings.tron_trx_commission,
            )
            await self.transfer(
                wallet.address,
                wallet.private_key,
                settings.main_wallet_config["base58check_address"],
                balance,
            )

            payment.status = PaymentStatus.SUCCESS
            await payment.save()

            wallet.status = TronWalletStatus.RECEIVED
            await wallet.save()

            await UserCorrectDAO.create_correct(payment.user.id, balance, Currency.USDT)

            return True

    async def transfer(
        self,
        from_address: str,
        from_private_key: str,
        to_address: str,
        amount: float,
    ) -> dict[str, Any]:
        async with AsyncTron(network=settings.tron_network) as client:
            contract = await client.get_contract(settings.usdt_trc20_address)
            txb = (
                contract.functions.transfer(to_address, amount)
                .with_owner(from_address)
                .fee_limit(settings.tron_fee_limit)
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
        async with AsyncTron(network=settings.tron_network) as client:
            txb = client.trx.transfer(
                from_address,
                to_address,
                amount,
            ).memo("test memo")
            txn = await txb.build()
            txn_ret = await txn.sign(from_private_key)
            return await txn_ret.wait()
