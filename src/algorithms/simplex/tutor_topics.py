from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpBinary, PULP_CBC_CMD


class TopicTutorAssignmentSimplexSolver:
    def __init__(self, groups, topics, tutors):
        """
        Constructor of the class.

        Args:
            - groups: List of groups.
            - tutors: List of tutors.
            - topics: List of topics.
        """
        self._groups = groups
        self._topics = topics
        self._tutors = tutors

    def _create_decision_variables(self):
        """
        Create decision variables.

        It iterates through each combination of groups, topics, and tutors,
        creating a binary decision variable for each combination.

        Returns a dictionary of decision variables.
        """
        assignment_vars = {}
        for i, group in enumerate(self._groups, 1):
            for topic in self._topics:
                for tutor in self._tutors:
                    assignment_vars[(i, topic.id, tutor.id)] = LpVariable(
                        f"Assignment_{i}_{topic.id}_{tutor.id}", 0, 1, LpBinary
                    )
        return assignment_vars

    def _create_optimization_problem(self):
        """
        Create the optimization problem.

        Returns an instance of the optimization problem.
        """
        return LpProblem("GroupAssignment", LpMaximize)

    def _add_objective_function(self, prob, assignment_vars):
        """
        Add the objective function to the optimization problem.

        Args:
            - prob: Instance of the optimization problem.
            - assignment_vars: Assignment variables.
        """
        topic_scores = {
            (i, topic.id): 0
            for i in range(1, len(self._groups) + 1)
            for topic in self._topics
        }
        for i, group in enumerate(self._groups, 1):
            for j, topic in enumerate(self._topics):
                topic_scores[(i, topic.id)] = len(self._topics) - j
        prob += lpSum(
            topic_scores[(i, topic.id)] * assignment_vars[(i, topic.id, tutor.id)]
            for i in range(1, len(self._groups) + 1)
            for topic in self._topics
            for tutor in self._tutors
        )

    def _add_constraints(self, prob, assignment_vars):
        """
        Add constraints for the simplex algorithm.

        Args:
            - prob: Instance of the optimization problem.
            - assignment_vars: Assignment variables.
        """
        self._add_group_assignment_constraints(prob, assignment_vars)
        self._add_topic_capacity_constraints(prob, assignment_vars)
        self._add_tutor_capacity_constraints(prob, assignment_vars)

    def _add_group_assignment_constraints(self, prob, assignment_vars):
        """
        Add constraints for group assignments.

        Args:
            - prob: Instance of the optimization problem.
            - assignment_vars: Assignment variables.
        """
        for i, group in enumerate(self._groups, 1):
            prob += (
                lpSum(
                    assignment_vars[(i, topic.id, tutor.id)]
                    for topic in self._topics
                    for tutor in self._tutors
                )
                <= 1
            )

    def _add_topic_capacity_constraints(self, prob, assignment_vars):
        """
        Add constraints for topic capacities.

        Args:
            - prob: Instance of the optimization problem.
            - assignment_vars: Assignment variables.
        """
        for topic in self._topics:
            for i in range(1, len(self._groups) + 1):
                prob += lpSum(
                    assignment_vars[(i, topic.id, tutor.id)] for tutor in self._tutors
                ) <= self._groups[i - 1].cost_of(topic)

    def _add_tutor_capacity_constraints(self, prob, assignment_vars):
        """
        Add constraints for tutor capacities.

        Args:
            - prob: Instance of the optimization problem.
            - assignment_vars: Assignment variables.
        """
        for tutor in self._tutors:
            assigned_topics = [topic.id for topic in self._topics]
            prob += (
                lpSum(
                    assignment_vars[(i, topic, tutor.id)]
                    for i in range(1, len(self._groups) + 1)
                    for topic in assigned_topics
                )
                <= tutor.capacity
            )

    def _solve_optimization_problem(self, prob):
        """
        Solve the optimization problem.

        Args:
            - prob: Instance of the optimization problem.

        Returns a list of selected variables.
        """
        prob.solve(PULP_CBC_CMD(msg=0))

        result_variables = []

        for var in prob.variables():
            if var.varValue == 1:
                result_variables.append(var.name)

        return result_variables

    def solve_simplex(self):
        """
        Solve the optimization problem using the simplex method.

        Args:
            - groups: List of groups.
            - tutors: List of tutors.
            - topics: List of topics.

        Returns a dictionary that represents the result of the assignment.
        """
        assignment_vars = self._create_decision_variables()

        prob = self._create_optimization_problem()
        self._add_objective_function(prob, assignment_vars)
        self._add_constraints(prob, assignment_vars)
        result = self._solve_optimization_problem(prob)
        return result
