from src.api.admins.exceptions import AdminNotInserted
from src.api.admins.schemas import AdminRequest
from src.api.exceptions import Duplicated
from src.api.users.models import Role, User


class AdminService:

    def __init__(self, repository) -> None:
        self._repository = repository

    def add_admin(self, hasher, admin: AdminRequest):
        """Agrega un nuevo usuario con rol de administrador usando el id como password"""
        try:
            return self._repository.add_user(
                User(
                    id=admin.id,
                    name=admin.name,
                    last_name=admin.last_name,
                    email=admin.email,
                    password=hasher.hash(str(admin.id)),
                    role=Role.ADMIN,
                )
            )
        except Duplicated as e:
            raise e
        except Exception:
            raise AdminNotInserted("Could not insert an admin in the database")
