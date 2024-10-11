from datetime import datetime, timedelta
from src.api.dates.exceptions import InvalidDate
from src.api.dates.models import DateSlot, GroupDateSlot, TutorDateSlot

from src.api.periods.exceptions import PeriodNotFound
from src.api.exceptions import EntityNotFound
from src.config.logging import logger


class DateSlotsService:

    def __init__(self, repository) -> None:
        self._repository = repository

    def _create_slots_from_ranges(self, ranges):
        HOURS = 60 * 60
        slots = list()
        for i in ranges:
            # Convert to datetime objects
            start = i.start
            end  = i.end
            hours_diff = (end - start).seconds // HOURS
            for hour in range(hours_diff ):
                diff = timedelta(hours=hour)
                slots.append(start + diff )

        return slots

    def add_slots(self, slot_ranges, period):
        try:
            slots = self._create_slots_from_ranges(slot_ranges)
            slots_to_save = [{"period_id": period, "slot": slot} for slot in slots]
            slots_saved = self._repository.add_bulk(DateSlot,slots_to_save)

            return slots_saved
        except Exception as e:
            logger.error(f"Could not update period because of: {str(e)}")
            raise InvalidDate(str(e))
        
    def add_group_slots(self, group_id, slot_ranges):
        try:
            slots = self._create_slots_from_ranges(slot_ranges)
            slots_to_save = [{"group_id": group_id, "slot": slot} for slot in slots]
            slots_saved = self._repository.add_bulk(GroupDateSlot,slots_to_save)

            return slots_saved
        except Exception as e:
            logger.error(f"Could not update period because of: {str(e)}")
            raise InvalidDate(str(e))
        
    def add_tutor_slots(self, tutor_id, period, slot_ranges):
        try:
            slots = self._create_slots_from_ranges(slot_ranges)
            slots_to_save = [{"tutor_id": tutor_id, "slot": slot, "period_id": period} for slot in slots]
            slots_saved = self._repository.add_bulk(TutorDateSlot,slots_to_save)

            return slots_saved
        except Exception as e:
            logger.error(f"Could not update period because of: {str(e)}")
            raise InvalidDate(str(e))
        
    def get_slots(self, period: str):
        return self._repository.get_slots_by_period(period)