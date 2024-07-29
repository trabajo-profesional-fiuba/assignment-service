import pytest
import datetime as dt
from sqlalchemy.orm import sessionmaker, scoped_session

from src.config.database import create_tables, drop_tables, engine
from src.api.form.repository import FormRepository
from src.api.form.schemas import GroupFormRequest
from src.api.form.exceptions import TopicNotFound
from src.api.users.repository import UserRepository
from src.api.users.schemas import UserResponse


class TestFormRepository:

    SessionFactory = sessionmaker(bind=engine)
    Session = scoped_session(SessionFactory)

    @pytest.fixture(scope="session")
    def tables(self):
        # Create all tables
        create_tables()
        yield
        # Drop all tables
        drop_tables()

    @pytest.mark.integration
    def test_add_group_form_with_topic_not_found(self, tables):
        today = dt.datetime.today().isoformat()
        group_form = GroupFormRequest(
            uid_sender=105001,
            uid_student_2=105002,
            uid_student_3=105003,
            uid_student_4=105004,
            group_id=today,
            topic_1="topic 1",
            topic_2="topic 2",
            topic_3="topic 3",
        )

        form_repository = FormRepository(self.Session)
        with pytest.raises(TopicNotFound):
            form_repository.add_group_form(group_form, [105001, 105002, 105003, 105004])

    @pytest.mark.integration
    def test_add_group_form_with_student_not_found(self, tables):
        student_1 = UserResponse(
            id=105001,
            name="Juan",
            last_name="Perez",
            email="email@fi,uba.ar",
            password="password",
        )
        student_2 = UserResponse(
            id=105002,
            name="Pedro",
            last_name="Pipo",
            email="email2@fi,uba.ar",
            password="password1",
        )
        student_3 = UserResponse(
            id=105003,
            name="Pepe",
            last_name="Bla",
            email="email3@fi,uba.ar",
            password="password1",
        )
        student_4 = UserResponse(
            id=105004,
            name="Maria",
            last_name="Lopez",
            email="mlopez4@fi.uba.ar",
            password="password1",
        )
        user_repository = UserRepository(self.Session)
        user_repository.add_students([student_1, student_2, student_3, student_4])

        today = dt.datetime.today().isoformat()
        group_form = GroupFormRequest(
            uid_sender=105001,
            uid_student_2=105002,
            uid_student_3=105003,
            uid_student_4=105004,
            group_id=today,
            topic_1="topic 1",
            topic_2="topic 2",
            topic_3="topic 3",
        )

        repository = FormRepository(self.Session)
        with pytest.raises(TopicNotFound):
            repository.add_group_form(group_form, [105001, 105002, 105003, 105004])
