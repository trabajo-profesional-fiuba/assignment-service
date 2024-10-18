from enum import Enum
import math

from src.api.groups.schemas import (
    AssignedDateResult,
    AssignedDateSlotResponse,
    AssignedGroupResponse,
    AssignmentResult,
)
from src.core.date_slots import DateSlot
from src.core.group import AssignedGroup, UnassignedGroup
from src.core.topic import Topic
from src.core.tutor import Tutor


class GroupTutorTopicAssignment:
    """Represents the assigment result"""

    def __init__(self, group: UnassignedGroup, tutor: Tutor, topic: Topic) -> None:
        self.group = group
        self.tutor = tutor
        self.topic = topic

    def relevance(self):
        i = next(
            (
                index
                for index, t in enumerate(self.group.topics)
                if t.id == self.topic.id
            ),
            3,
        )
        rel = 3 - i
        dcg = rel / math.log2(i + 2)

        return dcg

    def to_json(self):
        return AssignedGroupResponse(
            id=self.group.id,
            tutor={
                "id": self.tutor.id,
                "period_id": self.tutor.period_id,
                "name": self.tutor.name,
                "last_name": self.tutor.last_name,
                "email": self.tutor.email,
            },
            topic={
                "id": self.topic.id,
                "name": self.topic.name,
                "category": self.topic.category,
            },
        )


class GroupTutorTopicAssignmentResult:
    def __init__(
        self, status: int, assignments: list[GroupTutorTopicAssignment]
    ) -> None:
        self.status = status
        self.assignments = assignments

    def calculate_dcg(self):
        """Calcula https://en.m.wikipedia.org/wiki/Discounted_cumulative_gain

        Cada grupo tuvo asignado un tema, que ese tema tiene un DCG interno
        (es decir que tan relevante fue para ese grupo ese tema).
        La suma de todos los DCG / IDCG (Ideal, donde cada grupo tenga la mayor relevancia)
        Nos da la calidad del algoritmo. Tomamos cualquier tema que no forme parte del grupo
        como una relevancia 0 en i=4
        """
        result = 0.0
        if len(self.assignments) > 0:

            idcg = 3 * len(self.assignments)
            dcg = sum([assigment.relevance() for assigment in self.assignments])
            result = round(dcg / idcg, 3) * 100

        return result

    def add_assignment(self, assigment: GroupTutorTopicAssignment):
        self.assignments.append(assigment)

    def to_json(self):
        return AssignmentResult(
            status=self.status,
            assigment=[assignment.to_json() for assignment in self.assignments],
            dcg=self.calculate_dcg(),
        )


class DateSlotAssignment:
    def __init__(
        self, group_id: int, tutor_id: int, evaluator_id: int, date: DateSlot
    ) -> None:
        self.group_id = group_id
        self.tutor_id = tutor_id
        self.evaluator_id = evaluator_id
        self.date = date
        self.spanish_date = date.get_spanish_date()

    def to_json(self):
        return AssignedDateSlotResponse(
            group_id=self.group_id,
            tutor_id=self.tutor_id,
            evaluator_id=self.evaluator_id,
            date=self.date,
            spanish_date=self.spanish_date,
        )


class DateSlotsAssignmentResult:
    def __init__(self, status: int, assignment: DateSlotAssignment = None) -> None:
        self.status = status
        self.assignments = assignment

    def add_assignment(self, assigment: DateSlotAssignment):
        self.assignments.append(assigment)

    def to_json(self):
        return AssignedDateResult(
            status=self.status,
            assigment=[assignment.to_json() for assignment in self.assignments],
        )
