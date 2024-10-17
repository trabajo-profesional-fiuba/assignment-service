from datetime import timedelta
from src.api.dates.exceptions import InvalidDate
from src.api.dates.models import DateSlot, GroupDateSlot, TutorDateSlot
from src.config.logging import logger
from src.api.dates.schemas import DateSlotRequestList


class DateSlotsService:

    def __init__(self, repository) -> None:
        self._repository = repository

    def _create_slots_from_ranges(self, ranges):
        HOURS = 60 * 60
        slots = list()
        for i in ranges:
            # Convert to datetime objects
            start = i.start
            end = i.end
            hours_diff = (end - start).seconds // HOURS
            for hour in range(hours_diff):
                diff = timedelta(hours=hour)
                slots.append(start + diff)

        return slots

    def add_slots(self, slot_ranges, period):
        try:
            slots = self._create_slots_from_ranges(slot_ranges)
            slots_to_save = [{"period_id": period, "slot": slot} for slot in slots]
            slots_saved = self._repository.add_bulk(DateSlot, slots_to_save)

            return slots_saved
        except Exception as e:
            logger.error(f"Could not update period because of: {str(e)}")
            raise InvalidDate(str(e))

    def add_group_slots(self, group_id, slot_ranges):
        try:
            slots = self._create_slots_from_ranges(slot_ranges)
            slots_to_save = [{"group_id": group_id, "slot": slot} for slot in slots]
            slots_saved = self._repository.add_bulk(GroupDateSlot, slots_to_save)

            return slots_saved
        except Exception as e:
            logger.error(f"Could not update period because of: {str(e)}")
            raise InvalidDate(str(e))

    def add_tutor_slots(self, tutor_id, period, slot_ranges):
        try:
            slots = self._create_slots_from_ranges(slot_ranges)
            slots_to_save = [
                {"tutor_id": tutor_id, "slot": slot, "period_id": period}
                for slot in slots
            ]
            slots_saved = self._repository.add_bulk(TutorDateSlot, slots_to_save)

            return slots_saved
        except Exception as e:
            logger.error(f"Could not update period because of: {str(e)}")
            raise InvalidDate(str(e))

    def get_slots(self, period: str):
        return self._repository.get_slots_by_period(period)

    def get_tutors_slots_by_id(self, tutor_id: int, period: str):
        return self._repository.get_tutor_slots_by_id(tutor_id, period)

    def get_groups_slots_by_id(self, group_id: int):
        return self._repository.get_groups_slots_by_id(group_id)

    def sync_date_slots(self, slot_ranges: DateSlotRequestList, period: str):
        try:
            slots = self._create_slots_from_ranges(slot_ranges)
            slots_to_save = [{"period_id": period, "slot": slot} for slot in slots]
            self._repository.sync_date_slots(slots_to_save, period)
            return slots_to_save
        except Exception as e:
            logger.error(f"Could not update slots because of: {str(e)}")
            raise InvalidDate(str(e))

    def sync_group_slots(self, slot_ranges: DateSlotRequestList, group_id: int):
        try:
            slots = self._create_slots_from_ranges(slot_ranges)
            slots_to_save = [{"group_id": group_id, "slot": slot} for slot in slots]
            updated_slots = self._repository.sync_group_slots(slots_to_save, group_id)
            return slots_to_save
        except Exception as e:
            logger.error(f"Could not update group slots because of: {str(e)}")
            raise InvalidDate(str(e))

    def sync_tutor_slots(
        self, slot_ranges: DateSlotRequestList, tutor_id: int, period: str
    ):
        try:
            slots = self._create_slots_from_ranges(slot_ranges)
            slots_to_save = [
                {"tutor_id": tutor_id, "slot": slot, "period_id": period}
                for slot in slots
            ]
            updated_slots = self._repository.sync_tutor_slots(
                slots_to_save, tutor_id, period
            )
            return slots_to_save
        except Exception as e:
            logger.error(f"Could not update tutor slots because of: {str(e)}")
            raise InvalidDate(str(e))
