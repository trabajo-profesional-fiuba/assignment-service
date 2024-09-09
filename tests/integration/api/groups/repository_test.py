import pytest

from src.api.students.exceptions import StudentNotFound
from src.api.exceptions import Duplicated, EntityNotInserted, EntityNotFound
from src.api.groups.service import GroupService
from src.api.groups.repository import GroupRepository
from src.api.topics.models import Category, Topic
from src.api.topics.repository import TopicRepository
from src.api.tutors.models import Period
from src.api.tutors.repository import TutorRepository
from src.api.users.repository import UserRepository
from src.api.users.models import User, Role

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
    topic_repository.add_topics([Topic(name="nombre", category_id=1)])
    tutor_repository.add_period(Period(id="1C2025"))
    tutor = User(
        id=5,
        name="Pedro",
        last_name="Pipo",
        email="tutor@fi.uba.ar",
        password="password1",
        role=Role.TUTOR,
    )
    student1 = User(
        id=10000,
        name="Juan",
        last_name="Perez",
        email="10000@fi.uba.ar",
        password="password",
        role=Role.STUDENT,
    )
    student2 = User(
        id=2000,
        name="Pedro",
        last_name="Pipo",
        email="2000@fi.uba.ar",
        password="password1",
        role=Role.STUDENT,
    )
    u_repository.add_tutors([tutor])
    u_repository.add_students([student1, student2])
    tutor_repository.add_tutor_period(5, "1C2025")

    uids = [10000, 2000]
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
        id=3000,
        name="Juan",
        last_name="Perez",
        email="3000@fi.uba.ar",
        password="password",
        role=Role.STUDENT,
    )
    student2 = User(
        id=4000,
        name="Pedro",
        last_name="Pipo",
        email="4000@fi.uba.ar",
        password="password1",
        role=Role.STUDENT,
    )
    u_repository.add_students([student1, student2])

    uids = [3000, 4000]

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
        email="tutor1@fi.uba.ar",
        password="password1",
        role=Role.TUTOR,
    )
    student1 = User(
        id=100000,
        name="Juan",
        last_name="Perez",
        email="100000@fi.uba.ar",
        password="password",
        role=Role.STUDENT,
    )
    student2 = User(
        id=12000,
        name="Pedro",
        last_name="Pipo",
        email="12000@fi.uba.ar",
        password="password1",
        role=Role.STUDENT,
    )
    u_repository.add_tutors([tutor])
    u_repository.add_students([student1, student2])
    tutor_repository.add_tutor_period(6, "1C2025")

    uids = [100000, 12000]
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
        id=13000,
        name="Juan",
        last_name="Perez",
        email="13000@fi.uba.ar",
        password="password",
        role=Role.STUDENT,
    )
    student2 = User(
        id=14000,
        name="Pedro",
        last_name="Pipo",
        email="14000@fi.uba.ar",
        password="password1",
        role=Role.STUDENT,
    )
    u_repository.add_students([student1, student2])
    uids = [13000, 14000]

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
        email="tutor2@fi.uba.ar",
        password="password1",
        role=Role.TUTOR,
    )
    student1 = User(
        id=160000,
        name="Juan",
        last_name="Perez",
        email="16000@fi.uba.ar",
        password="password",
        role=Role.STUDENT,
    )
    student2 = User(
        id=17000,
        name="Pedro",
        last_name="Pipo",
        email="17000@fi.uba.ar",
        password="password1",
        role=Role.STUDENT,
    )
    u_repository.add_tutors([tutor])
    u_repository.add_students([student1, student2])
    tutor_repository.add_tutor_period(15, "1C2025")

    uids = [160000, 17000]
    tutor_period_id = 2
    topic_id = 1

    service = GroupService(repository)
    group = service.create_assigned_group(uids, tutor_period_id, topic_id, period_id="1C2025")
    ids = [user.id for user in group.students]

    assert ids == uids
    assert group.tutor_period_id == tutor_period_id
    assert group.topic_id == topic_id


@pytest.mark.integration
def test_add_new_group_with_three_topics_using_service(tables):
    repository = GroupRepository(Session)
    u_repository = UserRepository(Session)
    student1 = User(
        id=18000,
        name="Juan",
        last_name="Perez",
        email="18000@fi.uba.ar",
        password="password",
        role=Role.STUDENT,
    )
    student2 = User(
        id=19000,
        name="Pedro",
        last_name="Pipo",
        email="19000@fi.uba.ar",
        password="password1",
        role=Role.STUDENT,
    )
    u_repository.add_students([student1, student2])
    uids = [18000, 19000]

    service = GroupService(repository)
    group = service.create_basic_group(uids, [1, 2, 3], period_id="1C2025")
    ids = [user.id for user in group.students]
    expected_topics = [1, 2, 3]

    assert ids == uids
    assert len(group.preferred_topics) == 3
    assert all(t in expected_topics for t in group.preferred_topics)


@pytest.mark.integration
def test_add_student_cannot_be_with_one_that_is_not_a_user(tables):
    repository = GroupRepository(Session)
    u_repository = UserRepository(Session)
    student1 = User(
        id=200,
        name="Juan",
        last_name="Perez",
        email="200@fi.uba.ar",
        password="password",
        role=Role.STUDENT,
    )
    student2 = User(
        id=201,
        name="Pedro",
        last_name="Pipo",
        email="201@fi.uba.ar",
        password="password1",
        role=Role.STUDENT,
    )
    u_repository.add_students([student1, student2])
    uids = [200, 201]

    service = GroupService(repository)
    _ = service.create_basic_group(uids, [1, 2, 3], period_id="1C2025")
    with pytest.raises(EntityNotFound):
        _ = service.create_basic_group([200, 202], [1, 2, 3])


@pytest.mark.integration
def test_add_student_cannot_be_in_two_groups(tables):
    repository = GroupRepository(Session)
    u_repository = UserRepository(Session)
    student1 = User(
        id=203,
        name="Juan",
        last_name="Perez",
        email="203@fi.uba.ar",
        password="password",
        role=Role.STUDENT,
    )
    student2 = User(
        id=204,
        name="Pedro",
        last_name="Pipo",
        email="204@fi.uba.ar",
        password="password1",
        role=Role.STUDENT,
    )
    student3 = User(
        id=205,
        name="Pedro",
        last_name="Pipo",
        email="205@fi.uba.ar",
        password="password1",
        role=Role.STUDENT,
    )
    u_repository.add_students([student1, student2, student3])
    uids = [203, 204]

    service = GroupService(repository)
    _ = service.create_basic_group(uids, [1, 2, 3], period_id="1C2025")
    with pytest.raises(EntityNotInserted):
        _ = service.create_basic_group([203, 205], [1, 2, 3])

@pytest.mark.integration
def test_add_assigned_group_without_period(tables):
    uids = [160000, 17000]
    tutor_period_id = 2
    topic_id = 1
    
    repository = GroupRepository(Session)
    service = GroupService(repository)
    
    with pytest.raises(EntityNotInserted):
        service.create_assigned_group(uids, tutor_period_id, topic_id, period_id=None)