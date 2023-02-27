from typing import Optional

from guarantor.db.dao.base import BaseDAO
from guarantor.db.models.api_client import ApiClient


class ApiClientDAO(BaseDAO):
    _model = ApiClient

    @classmethod
    async def get_or_none(cls, token) -> Optional[ApiClient]:
        return await cls._model.get_or_none(token=token)
