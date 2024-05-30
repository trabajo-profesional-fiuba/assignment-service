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
        self._id = tutor_id
        self._available_dates = available_dates

    @property
    def id(self):
        return self._id

    @property
    def available_dates(self):
        return self._available_dates
