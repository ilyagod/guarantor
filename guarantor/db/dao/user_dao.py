from guarantor.db.dao.base import BaseDAO
from guarantor.db.models.user import User


class UserDAO(BaseDAO):
    _model = User
