from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

from guarantor.db.dao.api_client import ApiClientDAO
from guarantor.db.models.api_client import ApiClient

api_key_header = APIKeyHeader(name="api_key")


async def get_user_by_api_key(
    api_key: str = Security(api_key_header),
    api_client_dao: ApiClientDAO = Depends(),
) -> ApiClient:
    api_client = await api_client_dao.get(token=api_key)
    if not api_client:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Could not validate API KEY",
        )
    return api_client
