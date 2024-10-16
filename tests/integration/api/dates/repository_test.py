import pytest
import datetime as dt
from sqlalchemy.orm import sessionmaker, scoped_session

from src.api.dates.models import DateSlot, GroupDateSlot, TutorDateSlot
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

    @pytest.mark.integration
    def test_update_slots(self, tables):
        repository = DateSlotRepository(self.Session)
        period = "2C2024"
        slots_to_update = [
            {
                "period_id": period,
                "slot": dt.datetime(2024, 10, 15, 9, 0),
            },
            {
                "period_id": period,
                "slot": dt.datetime(2024, 10, 15, 10, 0),
            },
        ]
        repository.bulk_update_slots(slots_to_update, period)
        dates_saved = repository.get_slots_by_period(period)
        assert len(dates_saved) == 2

    @pytest.mark.integration
    def test_add_group_slots(self, tables):
        helper = ApiHelper()
        helper.create_student("Juan", "Perez", "105285", "juanperez@fi.uba.ar")
        helper.create_student_period("105285", "2C2024")
        helper.create_tutor("Tutor1", "Apellido", "1010", "email@fi.uba.ar")
        tutor_period = helper.create_tutor_period(1010, "2C2024", 1)
        topic = helper.create_topic("TopicCustom")
        group = helper.create_group(["105285"], tutor_period.id, topic.id, "2C2024")

        date_repository = DateSlotRepository(self.Session)
        data = [{"group_id": group.id, "slot": dt.datetime(2024, 10, 15, 9, 0)}]
        date_repository.add_bulk(GroupDateSlot, data)
        dates_saved = date_repository.get_groups_slots_by_id(group.id)
        assert len(dates_saved) == 1

    @pytest.mark.integration
    def test_update_group_slots(self, tables):
        date_repository = DateSlotRepository(self.Session)
        group_id = 1
        slots_to_update = [
            {"group_id": group_id, "slot": dt.datetime(2024, 10, 15, 10, 0)}
        ]
        date_repository.bulk_update_group_slots(slots_to_update, group_id)
        dates_saved = date_repository.get_groups_slots_by_id(group_id)
        assert len(dates_saved) == 1
        assert dates_saved[0].group_id == group_id
        assert dates_saved[0].slot == dt.datetime(2024, 10, 15, 10, 0)

    @pytest.mark.integration
    def test_add_tutor_slots(self, tables):
        tutor_id = 1010
        period = "2C2024"
        data = [
            {
                "period_id": period,
                "slot": dt.datetime(2024, 10, 15, 9, 0),
                "tutor_id": tutor_id,
            }
        ]

        date_repository = DateSlotRepository(self.Session)
        date_repository.add_bulk(TutorDateSlot, data)

        dates_saved = date_repository.get_tutor_slots_by_id(tutor_id, period)
        assert len(dates_saved) == 1

    @pytest.mark.integration
    def test_update_tutor_slots(self, tables):
        tutor_id = 1010
        period = "2C2024"
        slots_to_update = [
            {
                "period_id": period,
                "slot": dt.datetime(2024, 10, 15, 10, 0),
                "tutor_id": tutor_id,
            }
        ]

        date_repository = DateSlotRepository(self.Session)
        date_repository.bulk_update_tutor_slots(slots_to_update, tutor_id, period)

        dates_saved = date_repository.get_tutor_slots_by_id(tutor_id, period)
        assert len(dates_saved) == 1
        assert dates_saved[0].tutor_id == tutor_id
        assert dates_saved[0].slot == dt.datetime(2024, 10, 15, 10, 0)
