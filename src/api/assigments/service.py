


from src.core.algorithms.topic_tutor.incomplete_groups_lp_solver import IncompleteGroupsLPSolver
from src.core.group_answer import GroupFormAnswer


class AssigmentService:

    def assigment_incomplete_groups(self, answers):
        incompleted_groups = list()
        for a in answers:
            answer = GroupFormAnswer(
                id= a.id,
                students = a.students,
                topics = a.topics,
                )
            incompleted_groups.append(answer)

        assigment_model = IncompleteGroupsLPSolver(incompleted_groups)
        results = assigment_model.solve()
        return results

