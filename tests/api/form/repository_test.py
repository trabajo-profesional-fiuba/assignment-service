import pytest
import datetime as dt
from sqlalchemy.orm import sessionmaker, scoped_session

from src.config.database import create_tables, drop_tables, engine
from src.api.form.repository import FormRepository
from src.api.form.schemas import GroupFormRequest
from src.api.form.exceptions import TopicNotFound, StudentNotFound, DuplicatedAnswer
from src.api.topic.repository import TopicRepository
from src.api.topic.schemas import TopicRequest, CategoryRequest
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

    @pytest.fixture()
    def today(self):
        return dt.datetime.today().isoformat()

    @pytest.mark.integration
    def test_add_group_form_with_topic_not_found(self, tables, today):
        group_form = GroupFormRequest(
            uid_sender=105001,
            uid_student_2=105002,
            uid_student_3=105003,
            uid_student_4=105004,
            answer_id=today,
            topic_1="topic 1",
            topic_2="topic 2",
            topic_3="topic 3",
        )

        form_repository = FormRepository(self.Session)
        with pytest.raises(TopicNotFound):
            form_repository.add_group_form(group_form, [105001, 105002, 105003, 105004])

    @pytest.mark.integration
    def test_add_group_form_with_student_not_found(self, tables, today):
        category_1 = CategoryRequest(name="category 1")
        category_2 = CategoryRequest(name="category 2")
        category_3 = CategoryRequest(name="category 3")
        topic_repository = TopicRepository(self.Session)
        topic_repository.add_categories([category_1, category_2, category_3])

        topic_1 = TopicRequest(name="topic 1", category="category 1")
        topic_2 = TopicRequest(name="topic 2", category="category 2")
        topic_3 = TopicRequest(name="topic 3", category="category 3")
        topic_repository.add_topics([topic_1, topic_2, topic_3])

        group_form = GroupFormRequest(
            uid_sender=105001,
            uid_student_2=105002,
            uid_student_3=105003,
            uid_student_4=105004,
            answer_id=today,
            topic_1="topic 1",
            topic_2="topic 2",
            topic_3="topic 3",
        )

        repository = FormRepository(self.Session)
        with pytest.raises(StudentNotFound):
            repository.add_group_form(group_form, [105001, 105002, 105003, 105004])

    @pytest.mark.integration
    def test_verify_duplicated_answer(self, tables, today):
        student_1 = UserResponse(
            id=105001,
            name="Juan",
            last_name="Perez",
            email="email1@fi,uba.ar",
            password="password",
        )
        student_2 = UserResponse(
            id=105002,
            name="Juan",
            last_name="Perez",
            email="email2@fi,uba.ar",
            password="password",
        )
        student_3 = UserResponse(
            id=105003,
            name="Juan",
            last_name="Perez",
            email="email3@fi,uba.ar",
            password="password",
        )
        student_4 = UserResponse(
            id=105004,
            name="Juan",
            last_name="Perez",
            email="email4@fi,uba.ar",
            password="password",
        )
        user_repository = UserRepository(self.Session)
        user_repository.add_students([student_1, student_2, student_3, student_4])

        group_form = GroupFormRequest(
            uid_sender=105001,
            uid_student_2=105002,
            uid_student_3=105003,
            uid_student_4=105004,
            answer_id=today,
            topic_1="topic 1",
            topic_2="topic 2",
            topic_3="topic 3",
        )

        repository = FormRepository(self.Session)
        repository.add_group_form(group_form, [105001, 105002, 105003, 105004])
        with pytest.raises(DuplicatedAnswer):
            repository.add_group_form(group_form, [105001, 105002, 105003, 105004])

    @pytest.mark.integration
    def test_verify_not_duplicated_answer(self, tables, today):
        student_5 = UserResponse(
            id=105005,
            name="Juan",
            last_name="Perez",
            email="email5@fi,uba.ar",
            password="password",
        )
        user_repository = UserRepository(self.Session)
        user_repository.add_students([student_5])

        group_form = GroupFormRequest(
            uid_sender=105001,
            uid_student_2=105002,
            uid_student_3=105005,
            uid_student_4=None,
            answer_id=today,
            topic_1="topic 1",
            topic_2="topic 2",
            topic_3="topic 3",
        )

        repository = FormRepository(self.Session)
        response = repository.add_group_form(group_form, [105001, 105002, 105005])
        assert len(response) == 3

    @pytest.mark.integration
    def test_add_form_with_same_groups_but_diff_topics(self, tables, today):
        group_form = GroupFormRequest(
            uid_sender=105001,
            uid_student_2=105002,
            uid_student_3=105003,
            uid_student_4=105003,
            answer_id=today,
            topic_1="topic 2",
            topic_2="topic 3",
            topic_3="topic 1",
        )

        repository = FormRepository(self.Session)
        response = repository.add_group_form(
            group_form, [105001, 105002, 105003, 105004]
        )
        assert len(response) == 4
        response = repository.get_group_form_by_answer_id(today)
        assert len(response) == 4
        repository.delete_group_form_by_answer_id(today)
        result = repository.get_group_form_by_answer_id(today)
        assert len(result) == 0
