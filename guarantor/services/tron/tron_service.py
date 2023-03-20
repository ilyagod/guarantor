import httpx
from tronpy import AsyncTron

from guarantor.db.dao.tron_wallet_dao import TronWalletDAO
from guarantor.enums import Currency
from guarantor.settings import settings


class TronService:
    # def __init__(self):
    #    #self.client = Tron(network=settings.tron_network)

    async def generate_address(self):
        async with AsyncTron(network=settings.tron_network) as client:
            return client.generate_address()

    async def create_payment(
        self,
        gateway_id: int,
        amount: float,
        user_id: int,
        currency: Currency,
        payment_id: int,
    ):
        wallet = await self.generate_address()
        await TronWalletDAO.create(
            {
                "address": wallet["base58check_address"],
                "private_key": wallet["private_key"],
                "public_key": wallet["public_key"],
                "amount": amount,
                "payment_id": payment_id,
            }
        )
        return {"address": wallet["base58check_address"]}

    async def get_balance(self, address: str, token_type: str = 'usdt'):
        subdomain = f'{settings.tron_network}api' if settings.tron_network != 'mainnet' else 'api'
        async with httpx.AsyncClient() as client:
            r = await client.get(f'https://{subdomain}.tronscan.org/api/account/tokens'
                                 f'?address={address}')
            for token in r.json()['data']:
                if token['tokenAbbr'].lower() == token_type:
                    return token['quantity']
        return 0
