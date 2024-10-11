import pytest
import datetime as dt
from sqlalchemy.orm import sessionmaker, scoped_session

from src.api.dates.models import DateSlot
from src.api.dates.repository import DateSlotRepository
from src.config.database.database import create_tables, drop_tables, engine
from tests.integration.api.helper import ApiHelper


class TestDateRepository:
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
    def test_get_empty_list_of_slots(self, tables):
        helper = ApiHelper()
        period = "2C2024"
        helper.create_period(period)
        
        repository = DateSlotRepository(self.Session)
        dates_saved = repository.get_slots_by_period(period)
        assert len(dates_saved) == 0
        
    @pytest.mark.integration
    def test_insert_slot_into_dates(self, tables):
        # Arrange
        slot = dt.datetime(2024, 10, 8, 9, 0)
        period = "2C2024"

        repository = DateSlotRepository(self.Session)
        date = DateSlot(period_id=period, slot=slot)
        # Act
        date_saved = repository.add_date_slot(date)
        # Assert
        assert date_saved.period_id == date.period_id
        assert date_saved.slot == date.slot

    @pytest.mark.integration
    def test_bulk_insert_slot_into_dates(self, tables):
        # Arrange
        period = "2C2024"
        slots = [
            {
                "period_id": period,
                "slot": dt.datetime(2024, 10, 7, 16, 0),
            },
            {
                "period_id": period,
                "slot": dt.datetime(2024, 10, 7, 22, 0),
            },
            {
                "period_id": period,
                "slot": dt.datetime(2024, 10, 8, 14, 0),
            },
            {
                "period_id": period,
                "slot": dt.datetime(2024, 10, 8, 18, 0),
            },
        ]

        repository = DateSlotRepository(self.Session)
        dates_saved = repository.add_bulk(DateSlot, slots)
        assert len(dates_saved) == 4

    @pytest.mark.integration
    def test_get_list_of_slots_by_period(self, tables):
        repository = DateSlotRepository(self.Session)
        period = "2C2024"
        dates_saved = repository.get_slots_by_period(period)
        assert len(dates_saved) == 5