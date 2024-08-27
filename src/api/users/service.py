from src.api.users.repository import UserRepository
from src.api.users.exceptions import InvalidCredentials
from src.config.logging import logger


class UserService:

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def authenticate(self, email, hashed_password):
        user = self._repository.get_user_by_email(email)
        if user.password != hashed_password:
            logger.error(f"The email {email} introduced wrong answerd")
            raise InvalidCredentials(message="Email or password is incorrect")

        return user

