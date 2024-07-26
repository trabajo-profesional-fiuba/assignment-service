
from src.api.users.repository import UserRepository
from src.api.auth.hasher import ShaHasher



class StudentService:

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository
    
    def authenticate(self, email, hashed_password):
        user = self._repository.get_user_by_email(email)
        if user.password != hashed_password:
            #FIXME - mejorar esto.
            raise Exception("401")

        return user