import pytest

from src.config.database.database import create_tables, drop_tables, engine
from sqlalchemy.orm import sessionmaker, scoped_session

from src.api.users.repository import UserRepository
from src.api.users.exceptions import UserNotFound
from src.api.users.models import User, Role


class TestUserRepository:

    SessionFactory = sessionmaker(bind=engine)
    Session = scoped_session(SessionFactory)

    @pytest.fixture(scope="module")
    def tables(self):
        # Create all tables
        create_tables()
        yield
        # Drop all tables
        drop_tables()

    @pytest.mark.integration
    def test_get_user_by_id_with_success(self, tables):
        repository = UserRepository(self.Session)
        user = User(
            id="105600",
            name="Juan",
            last_name="Perez",
            email="email@fi.uba.ar",
            password="password",
            role=Role.STUDENT,
        )
        repository.add_user(user)

        response = repository.get_user_by_id(105600)
        assert response.name == "Juan"
        assert response.last_name == "Perez"
        assert response.email == "email@fi.uba.ar"
        assert response.role == Role.STUDENT

    @pytest.mark.integration
    def test_get_user_by_id_with_user_not_found(self, tables):
        repository = UserRepository(self.Session)

        with pytest.raises(UserNotFound):
            repository.get_user_by_id(105601)
