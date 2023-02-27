from typing import List

from guarantor.db.models.api_client import ApiClient
from guarantor.db.models.deal import Deal
from guarantor.web.api.v1.deals.schema import DealIncoming


class DealDTO:
    async def create_deal(self, deal: DealIncoming, api_client: ApiClient) -> Deal:
        return await Deal.create(api_client=api_client, **deal.dict(exclude_none=True))

    async def get_all(self, api_client: ApiClient) -> List[Deal]:
        return await Deal.filter(api_client=api_client)
