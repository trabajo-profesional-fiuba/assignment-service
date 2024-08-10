import pytest

from src.api.groups.service import GroupService
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


@pytest.mark.integration
def test_add_new_group_with_tutor_but_no_topic(tables):
    tutor_repository = TutorRepository(Session)
    repository = GroupRepository(Session)
    u_repository = UserRepository(Session)
    tutor = User(
        id=6,
        name="Pedro",
        last_name="Pipo",
        email="tutor1@fi,uba.ar",
        password="password1",
        role=Role.TUTOR,
    )
    student1 = User(
        id=10,
        name="Juan",
        last_name="Perez",
        email="10@fi,uba.ar",
        password="password",
        role=Role.STUDENT,
    )
    student2 = User(
        id=12,
        name="Pedro",
        last_name="Pipo",
        email="12@fi,uba.ar",
        password="password1",
        role=Role.STUDENT,
    )
    u_repository.add_tutors([tutor])
    u_repository.add_students([student1, student2])
    tutor_repository.add_tutor_period(6, "1C2025")

    uids = [10, 12]
    period_id = 2

    group = repository.add_group(uids, period_id)
    ids = [user.id for user in group.students]

    assert ids == uids
    assert group.tutor_period.id == period_id
    assert group.topic is None


@pytest.mark.integration
def test_add_new_group_with_three_topics(tables):
    repository = GroupRepository(Session)
    u_repository = UserRepository(Session)
    student1 = User(
        id=13,
        name="Juan",
        last_name="Perez",
        email="13@fi,uba.ar",
        password="password",
        role=Role.STUDENT,
    )
    student2 = User(
        id=14,
        name="Pedro",
        last_name="Pipo",
        email="14@fi,uba.ar",
        password="password1",
        role=Role.STUDENT,
    )
    u_repository.add_students([student1, student2])
    uids = [10, 12]

    group = repository.add_group(ids=uids, preferred_topics=[1, 2, 3])
    ids = [user.id for user in group.students]
    expected_topics = [1, 2, 3]

    assert ids == uids
    assert len(group.preferred_topics) == 3
    assert all(t in expected_topics for t in group.preferred_topics)


@pytest.mark.integration
def test_add_new_group_with_tutor_and_topic_using_service(tables):
    tutor_repository = TutorRepository(Session)
    repository = GroupRepository(Session)
    u_repository = UserRepository(Session)
    tutor = User(
        id=15,
        name="Pedro",
        last_name="Pipo",
        email="tutor2@fi,uba.ar",
        password="password1",
        role=Role.TUTOR,
    )
    student1 = User(
        id=16,
        name="Juan",
        last_name="Perez",
        email="16@fi,uba.ar",
        password="password",
        role=Role.STUDENT,
    )
    student2 = User(
        id=17,
        name="Pedro",
        last_name="Pipo",
        email="17@fi,uba.ar",
        password="password1",
        role=Role.STUDENT,
    )
    u_repository.add_tutors([tutor])
    u_repository.add_students([student1, student2])
    tutor_repository.add_tutor_period(15, "1C2025")

    uids = [16,17]
    period_id = 2
    topic_id = 1
    
    service = GroupService(repository)
    group = service.create_assigned_group(uids, period_id, topic_id)
    ids = [user.id for user in group.students]

    assert ids == uids
    assert group.tutor_period_id == period_id
    assert group.topic_id == topic_id