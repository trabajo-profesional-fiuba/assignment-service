from datetime import datetime, timedelta
from src.api.dates.exceptions import InvalidDate
from src.api.dates.models import DateSlot

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
            slots_saved = self._repository.bulk_insert(slots_to_save)

            return slots_saved
        except Exception as e:
            logger.error(f"Could not update period because of: {str(e)}")
            raise InvalidDate(str(e))
