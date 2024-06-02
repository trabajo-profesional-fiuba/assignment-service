
class Evaluator:
    def __init__(self, id, avaliable_dates = []):
        self._id = id
        self._avaliable_dates = avaliable_dates
    

    @property
    def id(self):
        return self._id