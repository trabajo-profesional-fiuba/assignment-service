from src.config.logging import logger

from src.api.users.repository import UserRepository
from src.api.users.models import User
from src.api.exceptions import EntityNotFound
from src.api.users.exceptions import InvalidCredentials
from src.api.auth.jwt import InvalidJwt


class UserService:

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def authenticate(self, email, hashed_password):
        logger.info(f"The user with email: {email} is trying to log in")
        user = self._repository.get_user_by_email(email)
        if user.password != hashed_password:
            logger.error(f"The email {email} introduced wrong password")
            raise InvalidCredentials(message="Email or password is incorrect")

        return user

    def get_user_by_id(self, user_id: int):
        try:
            logger.info(f"Looking for information of user with id: {user_id}")
            return self._repository.get_user_by_id(user_id)
        except Exception as err:
            logger.error(f"Error when getting user {user_id} info: {err}")
            raise EntityNotFound("User not found")

    def validate_tutor(self, tutor_id: int, user: User):
        if tutor_id != user.id:
            raise InvalidJwt("User unauthorized")
