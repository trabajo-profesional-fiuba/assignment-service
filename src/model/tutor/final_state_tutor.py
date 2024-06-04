from src.model.delivery_date.delivery_date import DeliveryDate


class FinalStateTutor:

    def __init__(self, available_dates: list[DeliveryDate]) -> None:
        """
        Initializes the class with an id and a list of available_dates.
        Args:
            id: The unique identifier for the instance.
            available_dates: The list of `DeliveryDate`.
        Attributes:
            _available_dates: Stores the list of `DeliveryDate`.
        """
        self._available_dates = available_dates

    @property
    def available_dates(self) -> list[DeliveryDate]:
        return self._available_dates
