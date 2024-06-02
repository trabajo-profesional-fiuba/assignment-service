
class DeliveryDate:

    def __init__(self, week, day, hour):
        self._week = week
        self._day = day
        self._hour = hour
    

    def label(self):
        return f"{self._week}-{self._day}-{self._hour}"
    

    @property
    def week(self):
        return self._week
    
    @property
    def day(self):
        return self._day
    
    @property
    def hour(self):
        return self._hour