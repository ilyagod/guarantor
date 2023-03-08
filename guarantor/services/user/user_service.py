from guarantor.db.dao.user_dao import UserDAO
from guarantor.db.models.user import User


class UserService:
    async def create_or_update_user(self, name: str, external_id: int) -> User:
        user, created = await UserDAO.update_or_create(
            {"external_id": external_id},
            defaults={"name": name},
        )
        return user
