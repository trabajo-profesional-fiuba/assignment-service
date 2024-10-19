from src.core.date_slots import DateSlot

from src.api.dates.models import DateSlot as DateSlotModel


class DateSlotsMapper:

    @classmethod
    def map_model_to_date_slot(db_dates: list[DateSlotModel]):
        return [DateSlot(start_time=date.slot) for date in db_dates]
