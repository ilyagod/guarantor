from guarantor.db.dao.base import BaseDAO
from guarantor.db.models.api_client import ApiClient


class ApiClientDAO(BaseDAO):
    _model = ApiClient
