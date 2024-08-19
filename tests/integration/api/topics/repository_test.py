import pytest

from src.config.database.database import create_tables, drop_tables, engine
from sqlalchemy.orm import sessionmaker, scoped_session

from src.api.topic.repository import TopicRepository
from src.api.topic.models import Topic, Category


class TestTopicRepository:

    SessionFactory = sessionmaker(bind=engine)
    Session = scoped_session(SessionFactory)

    @pytest.fixture(scope="module")
    def tables(self):
        # Create all tables
        create_tables()
        yield
        # Drop all tables
        drop_tables()

    @pytest.mark.integration
    def test_add_category_with_success(self, tables):
        categories = [Category(name="category 1")]

        t_repository = TopicRepository(self.Session)
        result = t_repository.add_categories(categories)
        assert len(result) == 1
        assert result[0].name == "category 1"

    @pytest.mark.integration
    def test_add_topic_with_success(self, tables):
        topics = [Topic(name="topic 1", category=2)]

        t_repository = TopicRepository(self.Session)
        result = t_repository.add_topics(topics)
        assert len(result) == 1
        assert result[0].name == "topic 1"
        assert result[0].topic_category.name == "category 1"

    @pytest.mark.integration
    def test_get_topics_with_success(self, tables):
        t_repository = TopicRepository(self.Session)
        result = t_repository.get_topics()
        assert len(result) == 1
        assert result[0].name == "topic 1"
        assert result[0].category == 2

    @pytest.mark.integration
    def test_delete_topics_with_success(self, tables):
        t_repository = TopicRepository(self.Session)
        t_repository.delete_topics()
        result = t_repository.get_topics()
        assert len(result) == 0
