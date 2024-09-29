import pytest

from src.core.group_form_answer import GroupFormAnswer
from src.core.topic import Topic


class TestGroupFormAnswer:

    @pytest.mark.unit
    def test_a_group_form_answer_can_have_empty_students_and_topics(self):
        group = GroupFormAnswer(id="id1")

        assert len(group.students) == 0
        assert len(group.topics) == 0

    @pytest.mark.unit
    def test_a_group_form_answer_can_not_have_duplicated_topics(self):
        topic = Topic(1, title="topic_title", category="category", capacity=1)
        group = GroupFormAnswer(id="id1", topics=[topic])
        topic_duplicated = Topic(
            1, title="topic_title", category="category", capacity=0
        )

        group.add_topics([topic_duplicated])

        assert len(group.topics) == 1

    @pytest.mark.unit
    def test_a_group_form_answer_returns_topics_ids(self):
        topic = Topic(1, title="first", category="category", capacity=1)
        topic2 = Topic(2, title="second", category="category", capacity=0)
        group = GroupFormAnswer(id="id1", topics=[topic, topic2])

        ids = group.get_topic_ids()

        assert len(group.topics) == 2
        assert all(id in [1, 2] for id in ids)

    @pytest.mark.unit
    def test_a_group_form_answer_returns_topics_names(self):
        topic = Topic(1, title="first", category="category", capacity=1)
        topic2 = Topic(2, title="second", category="category", capacity=0)
        group = GroupFormAnswer(id="id1", topics=[topic, topic2])

        names = group.get_topic_names()

        assert len(group.topics) == 2
        assert all(name in ["first", "second"] for name in names)
