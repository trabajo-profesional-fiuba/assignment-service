from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpBinary, PULP_CBC_CMD
import re

class SimplexSolver:
    def __init__(self, dates, groups, tutors, external_professors=None):
        self._dates = dates
        self._groups = groups
        self._tutors = tutors
        self._external_professors = external_professors

    def solve_simplex(self, groups, professors, topics):
        """
        Solve the simplex optimization problem.
        """
        prob = self._create_optimization_problem(groups, professors, topics)
        assignment_vars = self._create_decision_variables(groups, professors, topics)
        self._add_objective_function(prob, assignment_vars, groups, professors, topics)
        self._add_constraints(prob, assignment_vars, groups, professors, topics)
        result_variables = self._solve_optimization_problem(prob)
        result = self._get_results(result_variables)

        return result

    def _create_optimization_problem(self, groups, professors, topics):
        """
        Create the optimization problem.
        """
        return LpProblem("Group Assignment", LpMaximize)
    
    def _create_decision_variables(self, groups, professors, topics):
        """
        Create decision variables.
        """
        assignment_vars = {}
        for i, group in enumerate(groups, 1):
            for topic in topics:
                for professor in professors:
                    if topic[0] in professor[2]:
                        assignment_vars[(i, topic[0], professor[0])] = LpVariable(f"Asignación_{i}_{topic[0]}_{professor[0]}", 0, 1, LpBinary)
        return assignment_vars

    def _add_objective_function(self, prob, assignment_vars, groups, professors, topics):
        """
        Add the objective function to the optimization problem.
        """
        topic_scores = {(i, topic[0]): 0 for i in range(1, len(groups)+1) for topic in topics}
        for i, group in enumerate(groups, 1):
            for j, topic in enumerate(group[1]):
                topic_scores[(i, topic)] = len(group[1]) - j
        prob += lpSum(topic_scores[(i, topic[0])] * assignment_vars[(i, topic[0], professor[0])] for i in range(1, len(groups)+1) for topic in topics for professor in professors if topic[0] in professor[2])
    
    def _add_constraints(self,prob, assignment_vars, groups, professors, topics):
        """
        Add constraints for simplex algorithm.
        """
        self._add_group_assignment_constraints(prob, groups, professors, assignment_vars)
        self._add_topic_capacity_constraints(prob, topics, groups, professors, assignment_vars)
        self._add_professor_capacity_constraints(prob, professors, topics, groups, assignment_vars)

    def _add_group_assignment_constraints(self, prob, groups, professors, assignment_vars):
        """
        Add constraints for group assignments.
        """
        for i, group in enumerate(groups, 1):
            prob += lpSum(assignment_vars[(i, topic, professor[0])] for topic in group[1] for professor in professors if topic in professor[2]) == 1

    def _add_topic_capacity_constraints(self, prob, topics, groups, professors, assignment_vars):
        """
        Add constraints for topic capacities.
        """
        for topic in topics:
            prob += lpSum(assignment_vars[(i, topic[0], professor[0])] for i in range(1, len(groups)+1) for professor in professors if topic[0] in professor[2]) <= topic[1]['capacity']

    def _add_professor_capacity_constraints(self, prob, professors, topics, groups, assignment_vars):
        """
        Add constraints for professor capacities.
        """
        for professor in professors:
            assigned_topics = [topic[0] for topic in topics if topic[0] in professor[2]]
            prob += lpSum(assignment_vars[(i, topic, professor[0])] for i in range(1, len(groups)+1) for topic in assigned_topics) <= professor[1]['capacity']

    def _solve_optimization_problem(self, prob):
        """
        Solve the optimization problem.
        """
        prob.solve(PULP_CBC_CMD(msg=0))
        result_variables = []

        for var in prob.variables():
            if var.varValue == 1:
                result_variables.append(var.name)
        
        return result_variables

    def _get_results(self, result: {}):
        """Returns algorithm results."""
        original_dict = {}
        pattern = re.compile(r'Asignación_(\d+)_(\w+)_(\w+)')
        for var_name in result:
            match = pattern.match(var_name)
            if match:
                i, topic, professor = match.groups()
                i = int(i)
                if i not in original_dict:
                    original_dict[i] = {}
                original_dict[i][topic] = professor

        return original_dict