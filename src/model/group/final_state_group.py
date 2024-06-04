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

    def filter_dates(self, dates):
        labels = [d.label() for d in self._available_dates]
        possible_dates = []
        for date in dates:
            if date.label() in labels:
                possible_dates.append(date)
        return possible_dates

    def remove_dates(self, dates):
        for date in self._available_dates:
            if date.label() in dates:
                self._available_dates.remove(date)
