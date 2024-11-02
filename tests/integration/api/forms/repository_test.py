import pytest
import datetime as dt
from sqlalchemy.orm import sessionmaker, scoped_session

from src.api.students.exceptions import StudentNotFound
from src.api.topics.exceptions import TopicNotFound
from src.config.database.database import create_tables, drop_tables, engine
from src.api.forms.repository import FormRepository
from src.api.exceptions import Duplicated
from src.api.topics.repository import TopicRepository
from src.api.topics.models import Topic, Category
from src.api.users.repository import UserRepository
from src.api.users.models import User, Role
from src.core.student_form_answer import StudentFormAnswer
from tests.integration.api.helper import ApiHelper


class TestFormRepository:

    SessionFactory = sessionmaker(bind=engine)
    Session = scoped_session(SessionFactory)

    @pytest.fixture(scope="module")
    def tables(self):
        # Create all tables
        create_tables()
        yield
        # Drop all tables
        drop_tables()

    @pytest.fixture
    def today(self):
        return dt.datetime.today().isoformat()

    @pytest.fixture
    def answers(self, today):
        topics = ["topic 1", "topic 2", "topic 3"]
        answers = [
            StudentFormAnswer(id=105001, answer_id=today, topics=topics),
            StudentFormAnswer(id=105002, answer_id=today, topics=topics),
            StudentFormAnswer(id=105003, answer_id=today, topics=topics),
            StudentFormAnswer(id=105004, answer_id=today, topics=topics),
        ]
        return answers

    @pytest.mark.integration
    def test_add_answers_with_topic_not_found(self, tables, today, answers):
        form_repository = FormRepository(self.Session)
        with pytest.raises(TopicNotFound):
            form_repository.add_answers(
                answers,
                ["topic 1", "topic 2", "topic 3"],
                [105001, 105002, 105003, 105004],
                "1C2024",
            )

    @pytest.mark.integration
    def test_add_answers_with_student_not_found(self, tables, today, answers):
        category_1 = Category(name="category 1")
        category_2 = Category(name="category 2")
        category_3 = Category(name="category 3")
        topic_repository = TopicRepository(self.Session)
        topic_repository.add_categories([category_1, category_2, category_3])

        topic_1 = Topic(name="topic 1", category_id=2)
        topic_2 = Topic(name="topic 2", category_id=3)
        topic_3 = Topic(name="topic 3", category_id=4)
        topic_repository.add_topics([topic_1, topic_2, topic_3])

        topics = ["topic 1", "topic 2", "topic 3"]
        user_ids = [105001, 105002, 105003, 105004]
        repository = FormRepository(self.Session)
        with pytest.raises(StudentNotFound):
            repository.add_answers(answers, topics, user_ids, "1C2024")

    @pytest.mark.integration
    def test_add_answers_with_success(self, tables, today, answers):
        helper = ApiHelper()
        helper.create_period("1C2024")
        student_1 = User(
            id=105001,
            name="Juan",
            last_name="Perez",
            email="email1@fi.uba.ar",
            password="password",
            role=Role.STUDENT,
        )
        student_2 = User(
            id=105002,
            name="Juan",
            last_name="Perez",
            email="email2@fi.uba.ar",
            password="password",
            role=Role.STUDENT,
        )
        student_3 = User(
            id=105003,
            name="Juan",
            last_name="Perez",
            email="email3@fi.uba.ar",
            password="password",
            role=Role.STUDENT,
        )
        student_4 = User(
            id=105004,
            name="Juan",
            last_name="Perez",
            email="email4@fi.uba.ar",
            password="password",
            role=Role.STUDENT,
        )
        user_repository = UserRepository(self.Session)
        user_repository.add_students([student_1, student_2, student_3, student_4])

        repository = FormRepository(self.Session)
        topics = ["topic 1", "topic 2", "topic 3"]
        user_ids = [105001, 105002, 105003, 105004]
        result = repository.add_answers(answers, topics, user_ids, "1C2024")
        assert len(result) == 4

    @pytest.mark.integration
    def test_add_duplicated_answers(self, tables, today, answers):
        repository = FormRepository(self.Session)
        topics = ["topic 1", "topic 2", "topic 3"]
        user_ids = [105001, 105002, 105003, 105004]
        with pytest.raises(Duplicated):
            repository.add_answers(answers, topics, user_ids, "1C2024")

    @pytest.mark.integration
    def test_verify_not_duplicated_answer(self, tables, today):
        student_5 = User(
            id=105005,
            name="Juan",
            last_name="Perez",
            email="email5@fi.uba.ar",
            password="password",
            role=Role.STUDENT,
        )
        user_repository = UserRepository(self.Session)
        user_repository.add_students([student_5])
        answers = [
            StudentFormAnswer(
                id=105001, answer_id=today, topics=["topic 1", "topic 2", "topic 3"]
            ),
            StudentFormAnswer(
                id=105002, answer_id=today, topics=["topic 1", "topic 2", "topic 3"]
            ),
            StudentFormAnswer(
                id=105005, answer_id=today, topics=["topic 1", "topic 2", "topic 3"]
            ),
        ]

        repository = FormRepository(self.Session)
        response = repository.add_answers(
            answers,
            ["topic 1", "topic 2", "topic 3"],
            [105001, 105002, 105005],
            "1C2024",
        )
        assert len(response) == 3

    @pytest.mark.integration
    def test_add_answers_with_same_groups_but_diff_topics(self, tables, today):
        answers = [
            StudentFormAnswer(
                id=105001, answer_id=today, topics=["topic 2", "topic 3", "topic 1"]
            ),
            StudentFormAnswer(
                id=105002, answer_id=today, topics=["topic 2", "topic 3", "topic 1"]
            ),
            StudentFormAnswer(
                id=105003, answer_id=today, topics=["topic 2", "topic 3", "topic 1"]
            ),
            StudentFormAnswer(
                id=105004, answer_id=today, topics=["topic 2", "topic 3", "topic 1"]
            ),
        ]

        repository = FormRepository(self.Session)
        response = repository.add_answers(
            answers,
            ["topic 2", "topic 3", "topic 1"],
            [105001, 105002, 105003, 105004],
            "1C2024",
        )
        response = repository.get_answers_by_answer_id(today)
        assert len(response) == 4
        repository.delete_answers_by_answer_id(today)
        result = repository.get_answers_by_answer_id(today)
        assert len(result) == 0

    @pytest.mark.integration
    def test_get_answers_with_success(self, tables, today):
        repository = FormRepository(self.Session)
        response = repository.get_answers("1C2024")
        assert len(response) == 7

    @pytest.mark.integration
    def test_get_answers_by_user_id(self, tables):
        topic_repository = TopicRepository(self.Session)
        repository = FormRepository(self.Session)
        user_repository = UserRepository(self.Session)
        student = User(
            id=101010,
            name="Juan",
            last_name="Perez",
            email="101010@fi.uba.ar",
            password="password",
            role=Role.STUDENT,
        )
        topic_4 = Topic(name="topic 4", category_id=2)
        topic_5 = Topic(name="topic 5", category_id=3)
        topic_6 = Topic(name="topic 6", category_id=4)
        topic_repository.add_topics([topic_4, topic_5, topic_6])
        user_repository.add_students([student])
        today = dt.datetime.today().isoformat()
        answers = [
            StudentFormAnswer(
                id=101010, answer_id=today, topics=["topic 2", "topic 3", "topic 1"]
            ),
        ]

        repository.add_answers(
            answers, ["topic 2", "topic 3", "topic 1"], [101010], "1C2024"
        )
        today = dt.datetime.today().isoformat()
        answers = [
            StudentFormAnswer(
                id=101010, answer_id=today, topics=["topic 2", "topic 3", "topic 1"]
            )
        ]
        repository.add_answers(
            answers, ["topic 4", "topic 5", "topic 6"], [101010], "1C2024"
        )
        today = dt.datetime.today().isoformat()
        answers = [
            StudentFormAnswer(
                id=101010, answer_id=today, topics=["topic 1", "topic 2", "topic 4"]
            ),
        ]
        repository.add_answers(
            answers, ["topic 1", "topic 2", "topic 4"], [101010], "1C2024"
        )

        answers = repository.get_answers_by_user_id(101010, "1C2024")
        assert len(answers) == 3
