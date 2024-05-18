class Evaluator:

    def __init__(self, id: str, avaliable_dates: list):
        self._id = id
        self._avaliable_dates = avaliable_dates

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def avaliable_dates(self):
        return self._avaliable_dates

    def find_avaliable_dates(self, dates: list):
        return list(set(dates) & set(self._avaliable_dates))
