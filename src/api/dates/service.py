from datetime import datetime, timedelta

from src.api.dates.exceptions import InvalidDate
from src.api.dates.models import DateSlot, GroupDateSlot, TutorDateSlot
from src.api.dates.schemas import DateSlotRequestList
from src.config.logging import logger


class DateSlotsService:

    def __init__(self, repository) -> None:
        self._repository = repository

    def _create_slots_from_ranges(self, ranges):
        """Dado dos rangos, crea slots individuales por hora"""
        HOURS = 3600
        slots = list()
        for i in ranges:
            start = i.start
            end = i.end
            hours_diff = (end - start).seconds // HOURS
            for hour in range(hours_diff):
                diff = timedelta(hours=hour)
                slots.append(start + diff)

        return slots

    def add_slots(self, slot_ranges, period):
        """Agrega nuevas filas de slots asociadas a un cuatrimestre"""
        try:
            slots = self._create_slots_from_ranges(slot_ranges)
            slots_to_save = [{"period_id": period, "slot": slot} for slot in slots]
            slots_saved = self._repository.add_bulk(DateSlot, slots_to_save)

            return slots_saved
        except Exception as e:
            logger.error(f"Could not update period because of: {str(e)}")
            raise InvalidDate(str(e))

    def add_group_slots(self, group_id, slot_ranges):
        """Agrega nuevas filas de slots asociadas a un grupo"""
        try:
            slots = self._create_slots_from_ranges(slot_ranges)
            slots_to_save = [{"group_id": group_id, "slot": slot} for slot in slots]
            slots_saved = self._repository.add_bulk(GroupDateSlot, slots_to_save)

            return slots_saved
        except Exception as e:
            logger.error(f"Could not update period because of: {str(e)}")
            raise InvalidDate(str(e))

    def add_tutor_slots(self, tutor_id, period, slot_ranges):
        """Agrega nuevas filas de slots asociadas a un tutor y cuatrimestre"""
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

    def get_slots(self, period: str, only_available=False):
        """Obtiene todos los slots disponibles filtrando por only_available si quiere los asignados tambien o no"""
        return self._repository.get_slots_by_period(period, only_available)

    def get_tutors_slots_by_id(self, tutor_id: int, period: str):
        """Obtiene todos los slots de un tutor en un cuatrimestre"""
        return self._repository.get_tutor_slots_by_id(tutor_id, period)

    def get_groups_slots_by_id(self, group_id: int):
        """Obtiene todos los de un grupo"""
        return self._repository.get_groups_slots_by_id(group_id)

    def sync_date_slots(self, slot_ranges: DateSlotRequestList, period: str):
        """Sobreescribe los slots disponibles"""
        try:
            slots = self._create_slots_from_ranges(slot_ranges)
            slots_to_save = [{"period_id": period, "slot": slot} for slot in slots]
            self._repository.sync_date_slots(slots_to_save, period)

            return slots_to_save
        except Exception as e:
            logger.error(f"Could not update slots because of: {str(e)}")
            raise InvalidDate(str(e))

    def sync_group_slots(self, slot_ranges: DateSlotRequestList, group_id: int):
        """Sobreescribe los slots de un grupo"""
        try:
            slots = self._create_slots_from_ranges(slot_ranges)
            slots_to_save = [{"group_id": group_id, "slot": slot} for slot in slots]
            self._repository.sync_group_slots(slots_to_save, group_id)

            return slots_to_save
        except Exception as e:
            logger.error(f"Could not update group slots because of: {str(e)}")
            raise InvalidDate(str(e))

    def sync_tutor_slots(
        self, slot_ranges: DateSlotRequestList, tutor_id: int, period: str
    ):
        """Sobreescribe los slots de un tutor en un cuatrimestre"""
        try:
            slots = self._create_slots_from_ranges(slot_ranges)
            slots_to_save = [
                {"tutor_id": tutor_id, "slot": slot, "period_id": period}
                for slot in slots
            ]
            self._repository.sync_tutor_slots(slots_to_save, tutor_id, period)
            return slots_to_save
        except Exception as e:
            logger.error(f"Could not update tutor slots because of: {str(e)}")
            raise InvalidDate(str(e))

    def assign_tutors_dates(self, tutor_id: int, date: datetime, type: str):
        """Updatea las fechas de tutores a asignadas con el tipo"""
        try:
            attributes = {"assigned": True, "tutor_or_evaluator": type}
            self._repository.update_tutor_dates(tutor_id, date, attributes)
        except Exception as e:
            logger.error(f"Could not update tutor slots because of: {str(e)}")
            raise InvalidDate(str(e))

    def assign_date(self, date: datetime):
        """Marca una fecha como ya asignada"""
        try:
            attributes = {"assigned": True}
            self._repository.update_date(date, attributes)
        except Exception as e:
            logger.error(f"Could not update tutor slots because of: {str(e)}")
            raise InvalidDate(str(e))

    def get_assigned_dates(self, period_id):
        """Busca las fechas asignadas realizando joins"""
        return self._repository.get_assigned_dates()
