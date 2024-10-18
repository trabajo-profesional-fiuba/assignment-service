import pytest
from datetime import datetime

from src.core.date_slots import DateSlot
from src.core.delivery_date import DeliveryDate
from src.core.student import Student
from src.core.topic import Topic
from src.core.tutor import Tutor
from src.core.group import Group, AssignedGroup


class TestTutor:

    @pytest.fixture
    def assigned_groups_sample(self):

        students1 = [
            Student(id=1, name="Alice", last_name="Alan", email="alice@fi.uba.ar"),
            Student(id=2, name="Bob", last_name="Alan", email="bob@fi.uba.ar"),
        ]
        students2 = [
            Student(id=3, name="Juan", last_name="Alan", email="juan@fi.uba.ar"),
            Student(id=4, name="Boby", last_name="Alan", email="boby@fi.uba.ar"),
        ]

        topic1 = (Topic(id=1, title="Math", capacity=5, category="UBA"),)
        topic2 = (Topic(id=2, title="Science", capacity=10, category="UBA"),)

        dates1 = [
            DateSlot(start_time=datetime(2024, 10, 15, 0, 0, 0)),
            DateSlot(start_time=datetime(2024, 10, 16, 0, 0, 0)),
        ]
        dates2 = [
            DateSlot(start_time=datetime(2024, 10, 17, 0, 0, 0)),
            DateSlot(start_time=datetime(2024, 10, 14, 0, 0, 0)),
        ]

        group1 = AssignedGroup(
            id=101,
            available_dates=dates1,
            topic_assigned=topic1,
            students=students1,
            reviewer_id=201,
        )
        group2 = AssignedGroup(
            id=102,
            available_dates=dates2,
            topic_assigned=topic2,
            students=students2,
            reviewer_id=202,
        )
        group3 = AssignedGroup(
            id=103,
            available_dates=dates1,
            topic_assigned=topic2,
            students=students1,
            reviewer_id=203,
        )
        group4 = AssignedGroup(
            id=104,
            available_dates=dates2,
            topic_assigned=topic1,
            students=students2,
            reviewer_id=204,
        )
        group5 = AssignedGroup(
            id=105,
            available_dates=dates1,
            topic_assigned=topic1,
            students=students2,
            reviewer_id=205,
        )

        return [group1, group2, group3, group4, group5]

    @pytest.mark.unit
    def test_initialization(self):
        tutor = Tutor(
            id=1,
            period_id="2C2024",
            name="John",
            last_name="Doe",
            email="john.doe@example.com",
        )
        assert tutor.id == 1
        assert tutor.period_id == "2C2024"
        assert tutor.name == "John"
        assert tutor.last_name == "Doe"
        assert tutor.email == "john.doe@example.com"
        assert tutor.capacity == 0
        assert tutor.topics == []

    @pytest.mark.unit
    def test_initialization_with_topics(self):
        topics = [
            Topic(id=1, title="Math", category="UBA"),
            Topic(id=2, title="Science", category="UBA"),
        ]
        tutor = Tutor(
            id=1,
            period_id="2C2024",
            name="John",
            last_name="Doe",
            email="john.doe@example.com",
            capacity=10,
            topics=topics,
        )

        assert tutor.id == 1
        assert tutor.period_id == "2C2024"
        assert tutor.name == "John"
        assert tutor.last_name == "Doe"
        assert tutor.email == "john.doe@example.com"
        assert tutor.capacity == 10
        assert tutor.topics == topics

    @pytest.mark.unit
    def test_topics_ids(self):
        topics = [
            Topic(id=1, title="Math", category="UBA"),
            Topic(id=2, title="Science", category="UBA"),
        ]
        tutor = Tutor(
            id=1,
            period_id="2C2024",
            name="John",
            last_name="Doe",
            email="john.doe@example.com",
            topics=topics,
        )
        topics_ids = tutor.topics_ids()
        assert topics_ids == [1, 2]

    @pytest.mark.unit
    def test_capacity_of_existing_topic(self):
        topics = [
            Topic(id=1, title="Math", capacity=5, category="UBA"),
            Topic(id=2, title="Science", capacity=10, category="UBA"),
        ]
        tutor = Tutor(
            id=1,
            period_id="2C2024",
            name="John",
            last_name="Doe",
            email="john.doe@example.com",
            topics=topics,
        )
        capacity = tutor.capacity_of(Topic(id=1, title="Math"))
        assert capacity == 5

    @pytest.mark.unit
    def test_capacity_of_non_existing_topic(self):
        topics = [
            Topic(id=1, title="Math", capacity=5, category="UBA"),
            Topic(id=2, title="Science", capacity=10, category="UBA"),
        ]
        tutor = Tutor(
            id=1,
            period_id="2C2024",
            name="John",
            last_name="Doe",
            email="john.doe@example.com",
            topics=topics,
        )
        capacity = tutor.capacity_of(Topic(id=3, title="History", category="UBA"))
        assert capacity == 0

    @pytest.mark.unit
    def test_add_groups_to_tutor(self, assigned_groups_sample):
        topics = [
            Topic(id=1, title="Math", capacity=5, category="UBA"),
            Topic(id=2, title="Science", capacity=10, category="UBA"),
        ]

        tutor = Tutor(
            id=1,
            period_id="2C2024",
            name="John",
            last_name="Doe",
            email="john.doe@example.com",
            topics=topics,
        )

        tutor.assign_groups(assigned_groups_sample)

        assert len(tutor.groups) == len(assigned_groups_sample)
