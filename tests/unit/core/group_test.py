import pytest
from datetime import datetime

from src.core.date_slots import DateSlot
from src.core.group import AssignedGroup, UnassignedGroup
from src.core.student import Student
from src.core.tutor import Tutor
from src.core.topic import Topic


class TestUnassignedGroup:

    @pytest.mark.unit
    def test_initialization(self):
        group = UnassignedGroup(id=1)

        assert group.id == 1
        assert group._students == []
        assert group._topics == []

    @pytest.mark.unit
    def test_initialization_with_students_and_topics(self):
        students = [
            Student(id=1, name="Alice", last_name="Alan", email="alice@fi.uba.ar"),
            Student(id=2, name="Bob", last_name="Alan", email="boby@fi.uba.ar"),
        ]
        topics = [
            Topic(id=1, title="Math", category="UBA"),
            Topic(id=2, title="Science", category="UBA"),
        ]
        group = UnassignedGroup(id=1, students=students, topics=topics)

        assert group.id == 1
        assert group._students == students
        assert group._topics == topics

    @pytest.mark.unit
    def test_preference_of_existing_topic(self):
        topics = [
            Topic(id=1, title="Math", category="UBA"),
            Topic(id=2, title="Science", category="UBA"),
        ]
        group = UnassignedGroup(id=1, topics=topics)
        preference = group.preference_of(Topic(id=1, title="Math", category="UBA"))

        assert preference == 10  # First topic, so preference is 1 * 10

    @pytest.mark.unit
    def test_preference_of_non_existing_topic(self):
        topics = [
            Topic(id=1, title="Math", category="UBA"),
            Topic(id=2, title="Science", category="UBA"),
        ]
        group = UnassignedGroup(id=1, topics=topics)
        preference = group.preference_of(Topic(id=3, title="History", category="UBA"))

        assert preference == 100  # Topic not in list, so preference is 100


class TestAssignedGroup:

    @pytest.mark.unit
    def test_initialization(self):
        group = AssignedGroup(id=1)
        assert group.id == 1
        assert group._tutor is None
        assert group._available_dates == []
        assert group._assigned_date is None
        assert group._assigned_topic is None
        assert group._students == []
        assert group._reviewer_id is None

    @pytest.mark.unit
    def test_initialization_with_parameters(self):
        tutor = Tutor(
            id=1, name="Carlos", email="dr.smith@example.com", last_name="Fontela"
        )
        students = [
            Student(id=1, name="Alice", last_name="Alan", email="alice@fi.uba.ar"),
            Student(id=2, name="Bob", last_name="Alan", email="boby@fi.uba.ar"),
        ]
        topic = Topic(id=1, title="Math", category="UBA")
        dates = [DateSlot(start_time=datetime(2024, 10, 15, 0, 0, 0))]
        group = AssignedGroup(
            id=1,
            tutor=tutor,
            available_dates=dates,
            topic_assigned=topic,
            students=students,
            reviewer_id=101,
        )

        assert group.id == 1
        assert group._tutor == tutor
        assert group._available_dates == dates
        assert group._assigned_date is None
        assert group._assigned_topic == topic
        assert group._students == students
        assert group._reviewer_id == 101

    @pytest.mark.unit
    def test_emails(self):
        students = [
            Student(id=1, name="Alice", last_name="Alan", email="alice@fi.uba.ar"),
            Student(id=2, name="Bob", last_name="Alan", email="boby@fi.uba.ar"),
        ]
        group = AssignedGroup(id=1, students=students)
        emails = group.emails()

        assert emails == ["alice@fi.uba.ar", "boby@fi.uba.ar"]

    @pytest.mark.unit
    def test_tutor_email(self):
        tutor = Tutor(
            id=1, name="Carlos", email="dr.smith@example.com", last_name="Fontela"
        )
        group = AssignedGroup(id=1, tutor=tutor)
        tutor_email = group.tutor_email()

        assert tutor_email == "dr.smith@example.com"

    @pytest.mark.unit
    def test_assign_tutor(self):
        tutor = Tutor(
            id=1, name="Carlos", email="dr.smith@example.com", last_name="Fontela"
        )
        group = AssignedGroup(id=1)
        group.assign_tutor(tutor)
        assert group._tutor == tutor

    @pytest.mark.unit
    def test_get_tutor_id(self):
        tutor = Tutor(
            id=1, name="Carlos", email="dr.smith@example.com", last_name="Fontela"
        )
        group = AssignedGroup(id=1, tutor=tutor)
        tutor_id = group.tutor_id()
        assert tutor_id == 1

    @pytest.mark.unit
    def test_get_tutor_email(self):
        tutor = Tutor(
            id=1, name="Carlos", email="dr.smith@example.com", last_name="Fontela"
        )
        group = AssignedGroup(id=1, tutor=tutor)
        email = group.tutor_email()
        assert email == "dr.smith@example.com"