import pytest
import datetime as dt
from sqlalchemy.orm import sessionmaker, scoped_session

from src.config.database import create_tables, drop_tables, engine
from src.api.form.repository import FormRepository
from src.api.form.schemas import GroupFormResponse
from src.api.form.exceptions import TopicNotFound


class TestFormRepository:

    SessionFactory = sessionmaker(bind=engine)
    Session = scoped_session(SessionFactory)

    @pytest.fixture(scope="session")
    def tables(self):
        # Create all tables
        create_tables()
        yield
        # Drop all tables
        drop_tables()

    @pytest.mark.integration
    def test_add_group_form(self, tables):
        today = dt.datetime.today().isoformat()
        group_form = GroupFormResponse(
            uid=123456,
            group_id=today,
            topic_1="topic 1",
            topic_2="topic 2",
            topic_3="topic 3",
        )

        uids = [123456, 123457, 123458, 123459]

        repository = FormRepository(self.Session)
        with pytest.raises(TopicNotFound):
            repository.add_group_form(group_form, uids)
