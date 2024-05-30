from src.model.group.base_group import BaseGroup


class FinalStateGroup(BaseGroup):

    def __init__(self, id: str, available_dates: list, tutor_id: str):
        """
        Initializes the class with an id and a dict of available_dates.

        Args:
            id: The unique identifier for the instance.
            available_dates: The list of `DeliveryDate`.

        Attributes:
            _available_dates: Stores the topics ordered by preference.
        """
        super().__init__(id)
        self._available_dates = available_dates
        self._tutor_id = tutor_id

    @property
    def tutor_id(self):
        return self._tutor_id

    @property
    def available_dates(self):
        return self._available_dates
