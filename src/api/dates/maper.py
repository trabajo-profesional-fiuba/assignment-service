from src.api.dates.models import DateSlot as DateSlotModel
from src.core.date_slots import DateSlot


class DateSlotsMapper:

    @staticmethod
    def map_model_to_date_slot(db_dates: list[DateSlotModel]):
        """Mapea una lista de fechas desde la base de datos hacia clases nativas de python"""
        return [DateSlot(start_time=date.slot) for date in db_dates]
