from src.model.utils.delivery_date import DeliveryDate


class Evaluator:
    def __init__(self, id: int, available_dates: list[DeliveryDate] = []) -> None:
        self._id = id
        self._available_dates = available_dates
        self._assigned_dates = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def available_dates(self) -> list[DeliveryDate]:
        return self._available_dates

    @property
    def assigned_dates(self) -> list[DeliveryDate]:
        return self._assigned_dates

    def filter_dates(self, dates: list[DeliveryDate]):
        labels = [d.label() for d in self._available_dates]
        possible_dates = []
        for date in dates:
            if date.label() in labels:
                possible_dates.append(date)
        return possible_dates

    def assign_date(self, date: DeliveryDate) -> None:
        self._assigned_dates.append(date)
