from tortoise.contrib.pydantic import pydantic_model_creator

from guarantor.db.models.user import User

UserCreateOrUpdateSchema = pydantic_model_creator(
    User, name="User Create", exclude=("id",)
)
UserResponseSchema = pydantic_model_creator(User, name="User Response", include=("id",))
