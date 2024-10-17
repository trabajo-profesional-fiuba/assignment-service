import pytest


from src.core.group import UnassignedGroup
from src.core.student import Student
from src.core.tutor import Tutor
from src.core.topic import Topic
from src.core.delivery_date import DeliveryDate


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
        
        assert preference ==  10  # First topic, so preference is 1 * 10

    @pytest.mark.unit
    def test_preference_of_non_existing_topic(self):
        topics = [Topic(id=1, title="Math", category="UBA"), Topic(id=2, title="Science", category="UBA")]
        group = UnassignedGroup(id=1, topics=topics)
        preference = group.preference_of(Topic(id=3, title="History", category="UBA"))
        
        assert preference == 100  # Topic not in list, so preference is 100
