from typing import Optional

from guarantor.db.models.api_client import ApiClient


class ApiClientDAO:
    async def get(self, *, token: str) -> Optional[ApiClient]:
        return await ApiClient.get_or_none(token=token)
