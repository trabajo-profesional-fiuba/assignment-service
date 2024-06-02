from src.model.utils.delivery_date import DeliveryDate
from src.model.tutor import Tutor


class FinalStateGroup:

    def __init__(self, avaliable_dates):
        self._avaliable_dates = avaliable_dates
        self._assigned_dates = []
    
    @property
    def avaliable_dates(self):
        return self._avaliable_dates
        
    def assign(self, date: DeliveryDate, group):
        """
        Assigns a date to the group.
        Double-Distpatch is performed

        Args:
            date: The date to be assigned to the group.
        """
        group.assign_date(date)

    def assign_date(self, date):
        self._assigned_dates.append(date)
    
