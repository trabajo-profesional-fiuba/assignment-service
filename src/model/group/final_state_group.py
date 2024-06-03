from src.model.utils.delivery_date import DeliveryDate


class FinalStateGroup:

    def __init__(self, available_dates):
        self._available_dates = available_dates
        self._assigned_dates = []

    @property
    def available_dates(self):
        return self._available_dates

    def assign(self, date: DeliveryDate, group):
        """
        Assigns a date to the group.
        Double-Dispatch is performed

        Args:
            date: The date to be assigned to the group.
        """
        group.assign_date(date)

    def assign_date(self, date):
        self._assigned_dates.append(date)
