import pytest

from src.api.student.repository import StudentRepository
from src.api.groups.repository import GroupRepository
from src.api.topic.models import Category, Topic
from src.api.topic.repository import TopicRepository
from src.api.tutors.model import Period
from src.api.tutors.repository import TutorRepository
from src.api.users.repository import UserRepository
from src.api.users.model import User, Role

from src.config.database.database import create_tables, drop_tables, engine
from sqlalchemy.orm import sessionmaker, scoped_session


@pytest.fixture(scope="module")
def tables():
    # Create all tables
    create_tables()
    yield
    # Drop all tables
    drop_tables()

SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

@pytest.mark.integration
def test_add_new_group_with_tutor_and_topic(tables):
    topic_repository = TopicRepository(Session)
    tutor_repository = TutorRepository(Session)
    repository = GroupRepository(Session)
    u_repository = UserRepository(Session)

    topic_repository.add_categories([Category(name="cat1")])
    topic_repository.add_topics([Topic(name="nombre", category="cat1")])
    tutor_repository.add_period(Period(id="1C2025"))
    tutor = User(
        id=5,
        name="Pedro",
        last_name="Pipo",
        email="tutor@fi,uba.ar",
        password="password1",
        role=Role.TUTOR,
    )
    student1 = User(
        id=1,
        name="Juan",
        last_name="Perez",
        email="1@fi,uba.ar",
        password="password",
        role=Role.STUDENT,
    )
    student2 = User(
        id=2,
        name="Pedro",
        last_name="Pipo",
        email="2@fi,uba.ar",
        password="password1",
        role=Role.STUDENT,
    )
    u_repository.add_tutors([tutor])
    u_repository.add_students([student1, student2])
    tutor_repository.add_tutor_period(5, "1C2025")

    uids = [1, 2]
    period_id = 1
    topic_id = 1

    group = repository.add_group(uids, period_id, topic_id)
    ids = [user.id for user in group.students]

    assert ids == uids
    assert group.tutor_period.id == period_id
    assert group.topic.id == topic_id

@pytest.mark.integration
def test_add_new_group_without_tutor_and_topic(tables):
    repository = GroupRepository(Session)
    u_repository = UserRepository(Session)
    student1 = User(
        id=3,
        name="Juan",
        last_name="Perez",
        email="3@fi,uba.ar",
        password="password",
        role=Role.STUDENT,
    )
    student2 = User(
        id=4,
        name="Pedro",
        last_name="Pipo",
        email="4@fi,uba.ar",
        password="password1",
        role=Role.STUDENT,
    )
    u_repository.add_students([student1, student2])

    uids = [3, 4]

    group = repository.add_group(uids)
    ids = [user.id for user in group.students]

    assert ids == uids
    assert group.tutor_period is None
    assert group.topic is None