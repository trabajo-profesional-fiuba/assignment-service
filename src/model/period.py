import src.model.tutor.tutor as tutor
from src.model.utils.delivery_date import DeliveryDate
from src.model.utils.topic import Topic
import src.model.group.group as group

import src.exceptions as e

class TutorPeriod:
    def __init__(self, period: str, tutor = None):
        self._period = period
        self._available_dates = []
        self._as_tutor_dates = []
        self._as_evaluator_dates = []
        self._substitute_dates = []
        self._groups = []
        self._topics = []
        self._is_evaluator = False
        self._tutor = tutor
        self._capacity = 0

    # Getters
    @property
    def available_dates(self):
        return self._available_dates

    @property
    def as_tutor_dates(self):
        return self._as_tutor_dates

    @property
    def as_evaluator_dates(self):
        return self._as_evaluator_dates

    @property
    def substitute_dates(self):
        return self._substitute_dates

    @property
    def groups(self):
        return self._groups

    @property
    def topics(self):
        return self._topics

    @property
    def tutor(self):
        return self._tutor

    @property
    def capacity(self):
        return self._capacity

    def period_name(self):
        return self._period

    def is_evaluator(self):
        return self._is_evaluator

    def add_parent(self, parent: 'tutor.Tutor'):
        self._tutor = parent
    
    def add_groups(self, groups: list['group.Group']):
        self._groups = groups
    
    def groups_ids(self):
        return [g.id() for g in self._groups]

    def id(self):
        if self._tutor:
            return self._tutor.id

        raise e.PeriodWithoutParentError('The period must have a parent')

    def make_evaluator(self):
        self._is_evaluator = True

    # Date manipulations
    def add_available_dates(self, dates: list[DeliveryDate]):
        self._available_dates += dates

    def evaluate_date(self, date: DeliveryDate):
        self._as_evaluator_dates.append(date)

    def tutor_date(self, date: DeliveryDate):
        self._as_tutor_dates.append(date)

    def is_avaliable(self, date: str):
        label = (d.label() for d in self._available_dates)
        return date in label

    def add_substitute_date(self, date: DeliveryDate):
        self._substitute_dates.append(date)

    def add_topic(self, topic: Topic):
        self._topics.append(topic)

    def find_mutual_dates(self, dates: list[DeliveryDate]):
        labels = [d.label() for d in dates]
        mutual_dates = list()

        for av in self._available_dates:
            available_date_label = av.label()
            if available_date_label in labels:
                mutual_dates.append(available_date_label)
        
        return mutual_dates
