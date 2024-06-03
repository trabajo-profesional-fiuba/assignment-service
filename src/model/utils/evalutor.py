
class Evaluator:
    def __init__(self, id, avaliable_dates = []):
        self._id = id
        self._avaliable_dates = avaliable_dates
    

    @property
    def id(self):
        return self._id

    @property
    def avaliable_dates(self):
        return self._avaliable_dates

    def filter_dates(self, dates):
        labels = [d.label() for d in self._avaliable_dates]
        possible_dates = []
        for date in dates:
            if date.label() in labels:
                possible_dates.append(date)
        return possible_dates