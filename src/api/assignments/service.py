from src.api.assignments.exceptions import MethodNotFound
from src.core.algorithms.topic_tutor.group_tutor_flow_solver import GroupTutorFlowSolver
from src.core.algorithms.topic_tutor.incomplete_groups_lp_solver import (
    IncompleteGroupsLPSolver,
)
from src.core.algorithms.topic_tutor.group_tutor_lp_solver import GroupTutorLPSolver


class AssignmentService:

    def assignment_incomplete_groups(self, answers):
        assigment_model = IncompleteGroupsLPSolver(answers)
        results = assigment_model.solve()
        return results

    def assignment_group_topic_tutor(
        self, groups, topics, tutors, balance_limit, method
    ):
        if method == "lp":
            assigment_model = GroupTutorLPSolver(groups, topics, tutors, balance_limit)
        elif method == "flow":
            assigment_model = GroupTutorFlowSolver(groups, topics, tutors)
        else:
            raise MethodNotFound('Method provided is unkown')
        
        results = assigment_model.solve()   
        return results
