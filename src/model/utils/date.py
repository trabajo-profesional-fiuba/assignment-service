class Date:
    def __init__(self, day: str, week: int, hours: list):
        self._day = day
        self._week = week
        self._hours = hours

    def __eq__(self, other):
        return isinstance(other, Date) and self.day == other.day and self.week == other.week
    
    def __repr__(self):
        return f"Date(day={self._day}, week={self._week}, hours={[hour.name for hour in self._hours]})"

    def __str__(self):
        return f"{self._day}, week {self._week}, hours: {[hour.name for hour in self._hours]}"
    
    @property
    def hours(self):
        return self._hours

    @property
    def day(self):
        return self._day
    
    @property
    def week(self):
        return self._week