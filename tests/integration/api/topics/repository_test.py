import pytest

from src.config.database.database import create_tables, drop_tables, engine
from sqlalchemy.orm import sessionmaker, scoped_session

from src.api.topics.repository import TopicRepository
from src.api.topics.models import Topic, Category


@pytest.fixture(scope="function")
def tables():
    # Create all tables
    create_tables()
    yield
    # Drop all tables
    drop_tables()


class TestTopicRepository:

    SessionFactory = sessionmaker(bind=engine)
    Session = scoped_session(SessionFactory)

    @pytest.mark.integration
    def test_add_category_with_success(self, tables):
        categories = [Category(name="category 1")]

        t_repository = TopicRepository(self.Session)
        result = t_repository.add_categories(categories)
        assert len(result) == 1
        assert result[0].name == "category 1"

    @pytest.mark.integration
    def test_add_topic_with_success(self, tables):
        categories = [Category(name="category 1")]
        topics = [Topic(name="topic 1", category_id=2)]

        t_repository = TopicRepository(self.Session)
        result = t_repository.add_categories(categories)
        result = t_repository.add_topics(topics)
        assert len(result) == 1
        assert result[0].name == "topic 1"
        assert result[0].category.name == "category 1"

    @pytest.mark.integration
    def test_get_topics_with_success(self, tables):
        categories = [Category(name="category 1")]
        topics = [Topic(name="topic 1", category_id=2)]
        t_repository = TopicRepository(self.Session)
        result = t_repository.add_categories(categories)
        result = t_repository.add_topics(topics)
        result = t_repository.get_topics()
        assert len(result) == 1
        assert result[0].name == "topic 1"

    @pytest.mark.integration
    def test_get_topic_by_id_with_success(self, tables):
        categories = [Category(name="category 1")]
        topics = [Topic(name="topic 1", category_id=2)]
        t_repository = TopicRepository(self.Session)
        result = t_repository.add_categories(categories)
        result = t_repository.add_topics(topics)
        result = t_repository.get_topic_by_id(1)
        assert result.name == "topic 1"

    @pytest.mark.integration
    def test_delete_topics_with_success(self, tables):
        t_repository = TopicRepository(self.Session)
        t_repository.delete_topics()
        result = t_repository.get_topics()
        assert len(result) == 0
