from src.core.algorithms.topic_tutor.incomplete_groups_lp_solver import (
    IncompleteGroupsLPSolver,
)


class AssignmentService:

    def assignment_incomplete_groups(self, answers):
        assigment_model = IncompleteGroupsLPSolver(answers)
        results = assigment_model.solve()
        return results
