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
    def test_insert_slot_into_dates(self, tables):
        helper = ApiHelper()
        helper.create_period("2C2024")
        
        slot = dt.datetime(2024, 10, 8, 9, 0)
        period = '2C2024'

        repository = DateSlotRepository(self.Session)
        date = DateSlot(period_id=period, slot=slot)

        date_saved = repository.add_date_slot(date)
        assert date_saved.period_id == date.period_id
        assert date_saved.slot == date.slot
