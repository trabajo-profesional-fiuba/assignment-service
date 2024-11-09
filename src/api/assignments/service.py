from src.api.assignments.exceptions import MethodNotFound
from src.core.algorithms.date.delivery_lp_solver import DeliveryLPSolver
from src.core.algorithms.topic_tutor.group_tutor_flow_solver import GroupTutorFlowSolver
from src.core.algorithms.topic_tutor.group_tutor_lp_solver import GroupTutorLPSolver
from src.core.algorithms.topic_tutor.incomplete_groups_lp_solver import (
    IncompleteGroupsLPSolver,
)
from src.core.result import DateSlotsAssignmentResult, GroupTutorTopicAssignmentResult


class AssignmentService:

    def assignment_incomplete_groups(self, answers):
        """Utiliza el algoritmo de programacion lineal para asignar los grupos"""
        assigment_model = IncompleteGroupsLPSolver(answers)
        results = assigment_model.solve()
        return results

    def assignment_group_topic_tutor(
        self, groups, topics, tutors, balance_limit, method
    ) -> GroupTutorTopicAssignmentResult:
        """
        Dependiendo el method utiliza el algoritmo de programacion lineal o de red de flujo para
        asignar grupos a temas de preferencias y a tutores
        """
        if method == "lp":
            assigment_model = GroupTutorLPSolver(groups, topics, tutors, balance_limit)
        elif method == "flow":
            assigment_model = GroupTutorFlowSolver(groups, topics, tutors)
        else:
            raise MethodNotFound("Method provided is unkown")

        results = assigment_model.solve()
        return results

    def assignment_dates(
        self,
        available_dates,
        tutors,
        evaluators,
        groups,
        max_groups_per_week,
        max_dif_evaluators,
    ) -> DateSlotsAssignmentResult:
        """
        Utiliza el algoritmo de programacion lineal de fechas para asignar grupos a fechas de exposicion
        """
        filtered_groups = list(filter(lambda x: x.assigned_date is None, groups))
        for t in tutors:
            if len(t.available_dates) == 0:
                t.available_dates = available_dates

        for e in evaluators:
            if len(e.available_dates) == 0:
                e.available_dates = available_dates

        assigment_model = DeliveryLPSolver(
            groups=filtered_groups,
            available_dates=available_dates,
            tutors=tutors,
            evaluators=evaluators,
            max_groups_per_week=max_groups_per_week,
            max_dif_evaluators=max_dif_evaluators,
        )
        results = assigment_model.solve()
        return results
