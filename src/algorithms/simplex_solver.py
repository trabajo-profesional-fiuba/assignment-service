from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpBinary, LpStatus

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
        topic_scores = self._calculate_topic_scores(groups, topics)
        self._add_objective_function(prob, assignment_vars, topic_scores)
        self._add_group_assignment_constraints(prob, groups, professors, assignment_vars)
        self._add_topic_capacity_constraints(prob, topics, groups, professors, assignment_vars)
        self._add_professor_capacity_constraints(prob, professors, topics, groups, assignment_vars)
        self._solve_optimization_problem(prob)

    def _create_optimization_problem(self, groups, professors, topics):
        """
        Create the optimization problem.
        """
        return LpProblem("Group Assignment", LpMaximize)

    def _create_decision_variables(self, groups, professors, topics):
        """
        Create decision variables.
        """
        return LpVariable.dicts(
            "Assignment",
             [(i, topic['topic'], professor['name'])
             for i in range(1, len(groups)+1)
             for topic in topics
             for professor in professors
             if topic['topic'] in professor['topics']], 0, 1, LpBinary)

    def _calculate_topic_scores(self, groups, topics):
        """
        Calculate topic scores based on group preferences.
        """
        topic_scores = {(i, topic['topic']): 0 for i in range(1, len(groups)+1) for topic in topics}
        for i, group in enumerate(groups, 1):
            for j, topic in enumerate(group):
                topic_scores[(i, topic)] = len(group) - j
        return topic_scores

    def _add_objective_function(self, prob, assignment_vars, topic_scores):
        """
        Add the objective function to the optimization problem.
        """
        prob += lpSum(topic_scores[(i, topic['topic'])] * assignment_vars[(i, topic['topic'], professor['name'])] for i in range(1, len(self._groups)+1) for topic in topics for professor in professors if topic['topic'] in professor['topics'])

    def _add_group_assignment_constraints(self, prob, groups, professors, assignment_vars):
        """
        Add constraints for group assignments.
        """
        for i, group in enumerate(groups, 1):
            prob += lpSum(assignment_vars[(i, topic, professor['name'])] for topic in group for professor in professors if topic in professor['topics']) == 1

    def _add_topic_capacity_constraints(self, prob, topics, groups, professors, assignment_vars):
        """
        Add constraints for topic capacities.
        """
        for topic in topics:
            prob += lpSum(assignment_vars[(i, topic['topic'], professor['name'])] for i in range(1, len(groups)+1) for professor in professors if topic['topic'] in professor['topics']) <= topic['capacity']

    def _add_professor_capacity_constraints(self, prob, professors, topics, groups, assignment_vars):
        """
        Add constraints for professor capacities.
        """
        for professor in professors:
            assigned_topics = [topic['topic'] for topic in topics if topic['topic'] in professor['topics']]
            prob += lpSum(assignment_vars[(i, topic, professor['name'])] for i in range(1, len(groups)+1) for topic in assigned_topics) <= professor['capacity']

    def _solve_optimization_problem(self, prob):
        """
        Solve the optimization problem.
        """
        prob.solve()
        print("Status:", LpStatus[prob.status])
        for var in prob.variables():  # Show decision variables with value 1
            if var.varValue == 1:
                print(f"{var.name}: {var.varValue}")

solver = SimplexSolver(dates, groups, tutors, external_professors)
solver.solve_simplex(groups, professors, topics)  # Run the optimization