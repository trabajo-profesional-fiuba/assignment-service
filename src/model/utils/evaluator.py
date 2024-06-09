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
        labels = [d.label() for d in dates]
        possible_dates = []
        possible_dates_labels = []
        for date in self._available_dates:
            if date.label() in labels:
                possible_dates.append(date)
                possible_dates_labels.append(date.label())
        self._available_dates = possible_dates
        return possible_dates_labels

    def assign_date(self, date: DeliveryDate) -> None:
        self._assigned_dates.append(date)

    def assign_dates(self, dates: list[DeliveryDate]):
        for d in dates:
            self.assign_date(d)

    def is_avaliable(self, date_label):
        labels = [d.label() for d in self._available_dates]
        return date_label in labels
