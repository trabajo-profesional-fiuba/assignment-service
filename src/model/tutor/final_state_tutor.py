class FinalStateTutor:

    def __init__(self, tutor_id: str, available_dates: list):
        """
        Initializes the class with an id and a list of available_dates.

        Args:
            id: The unique identifier for the instance.
            available_dates: The list of `DeliveryDate`.

        Attributes:
            _available_dates: Stores the list of `DeliveryDate`.
        """
        self._tutor_id = tutor_id
        self._available_dates = available_dates

    @property
    def tutor_id(self):
        return self._tutor_id

    @property
    def available_dates(self):
        return self._available_dates
