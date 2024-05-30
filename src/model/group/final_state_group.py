from src.model.group.base_group import BaseGroup


class FinalStateGroup(BaseGroup):

    def __init__(self, id: str, available_dates: dict, tutor_id: str):
        """
        Initializes the class with an id and a dict of available_dates.

        Args:
            id: The unique identifier for the instance.
            available_dates: The dict of available_dates ordered by preference.

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

    def is_tutored_by(self, tutor_id):
        return self._tutor_id == tutor_id

    def cost_of(self, date: str):
        return self._available_dates[date].priority

    def remove_dates(self, dates):
        for d in dates:
            date_label = d.label()
            if date_label in self._available_dates:
                del self._available_dates[date_label]
