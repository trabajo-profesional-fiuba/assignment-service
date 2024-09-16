import pytest

from src.config.database.database import create_tables, drop_tables, engine
from sqlalchemy.orm import sessionmaker, scoped_session

from tests.integration.api.helper import ApiHelper
from src.api.tutors.exceptions import PeriodNotFound
from src.api.periods.repository import PeriodRepository


class TestPeriodRepository:

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
    def test_get_all_periods_with_success(self, tables):
        helper = ApiHelper()
        helper.create_period("2C2024")

        p_repository = PeriodRepository(self.Session)
        response = p_repository.get_all_periods("DESC")
        assert len(response) == 1
        assert response[0].form_active is True
        assert response[0].initial_project_active is False
        assert response[0].intermediate_project_active is False
        assert response[0].final_project_active is False

    @pytest.mark.integration
    def test_get_existing_period_by_id(self, tables):
        p_repository = PeriodRepository(self.Session)
        response = p_repository.get_period_by_id("2C2024")
        assert response.id == "2C2024"

    @pytest.mark.integration
    def test_get_period_not_found_by_id(self, tables):
        p_repository = PeriodRepository(self.Session)

        with pytest.raises(PeriodNotFound):
            p_repository.get_period_by_id("3C2024")
