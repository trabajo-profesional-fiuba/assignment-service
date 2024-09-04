


from src.core.algorithms.topic_tutor.incomplete_groups_lp_solver import IncompleteGroupsLPSolver
from src.core.group_answer import GroupFormAnswer


class AssigmentService:

    def assigment_incomplete_groups(self, answers):
        assigment_model = IncompleteGroupsLPSolver(answers)
        results = assigment_model.solve()
        return results

