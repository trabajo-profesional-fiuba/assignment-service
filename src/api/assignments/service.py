from src.core.algorithms.topic_tutor.incomplete_groups_lp_solver import (
    IncompleteGroupsLPSolver,
)
from src.core.algorithms.topic_tutor.group_tutor_lp_solver import GroupTutorLPSolver
from src.core.algorithms.topic_tutor.incomplete_groups_lp_solver import (
    IncompleteGroupsLPSolver,
)


class AssignmentService:

    def assignment_incomplete_groups(self, answers):
        assigment_model = IncompleteGroupsLPSolver(answers)
        results = assigment_model.solve()
        return results

    def assignment_group_topic_tutor(self, groups, topics, tutors, balance_limit):
        assigment_model = GroupTutorLPSolver(groups, topics, tutors, balance_limit)
        results = assigment_model.solve()
        return results
