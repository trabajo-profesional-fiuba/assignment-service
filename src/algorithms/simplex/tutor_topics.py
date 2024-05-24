from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpBinary, PULP_CBC_CMD
import re

class TopicTutorAssignmentSimplexSolver:
    def __init__(self, groups, tutors, topics):
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

    def _create_optimization_problem(self):
        """
        Create the optimization problem.
        
        Returns an instance of the optimization problem.
        """
        return LpProblem("Group Assignment", LpMaximize)
    
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
        result_variables = self._solve_optimization_problem(prob)
        
        result = self._get_results(result_variables)

        return result

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
                    if topic[0] in tutor[2]:
                        assignment_vars[(i, topic[0], tutor[0])] = LpVariable(
                            f"Assignment_{i}_{topic[0]}_{tutor[0]}", 0, 1, LpBinary
                        )
        return assignment_vars

    def _add_objective_function(
        self, prob, assignment_vars
    ):
        """
        Add the objective function to the optimization problem.
        
        Args:
            - prob: Instance of the optimization problem.
            - assignment_vars: Assignment variables.
        """
        topic_scores = {
            (i, topic[0]): 0 for i in range(1, len(self._groups) + 1) for topic in self._topics
        }
        for i, group in enumerate(self._groups, 1):
            for j, topic in enumerate(group[1]):
                topic_scores[(i, topic)] = len(group[1]) - j
        prob += lpSum(
            topic_scores[(i, topic[0])] * assignment_vars[(i, topic[0], tutor[0])]
            for i in range(1, len(self._groups) + 1)
            for topic in self._topics
            for tutor in self._tutors
            if topic[0] in tutor[2]
        )

    def _add_constraints(self, prob, assignment_vars):
        """
        Add constraints for the simplex algorithm.
        
        Args:
            - prob: Instance of the optimization problem.
            - assignment_vars: Assignment variables.
        """
        self._add_group_assignment_constraints(
            prob, assignment_vars
        )
        self._add_topic_capacity_constraints(
            prob, assignment_vars
        )
        self._add_tutor_capacity_constraints(
            prob, assignment_vars
        )

    def _add_group_assignment_constraints(
        self, prob, assignment_vars
    ):
        """
        Add constraints for group assignments.
        
        Args:
            - prob: Instance of the optimization problem.
            - assignment_vars: Assignment variables.
        """
        for i, group in enumerate(self._groups, 1):
            prob += (
                lpSum(
                    assignment_vars[(i, topic, tutor[0])]
                    for topic in group[1]
                    for tutor in self._tutors
                    if topic in tutor[2]
                )
                <= 1
            )

    def _add_topic_capacity_constraints(
        self, prob, assignment_vars
    ):
        """
        Add constraints for topic capacities.
        
        Args:
            - prob: Instance of the optimization problem.
            - assignment_vars: Assignment variables.
        """
        for topic in self._topics:
            prob += (
                lpSum(
                    assignment_vars[(i, topic[0], tutor[0])]
                    for i in range(1, len(self._groups) + 1)
                    for tutor in self._tutors
                    if topic[0] in tutor[2]
                )
                <= topic[1]["capacity"]
            )

    def _add_tutor_capacity_constraints(
        self, prob, assignment_vars
    ):
        """
        Add constraints for tutor capacities.
        
        Args:
            - prob: Instance of the optimization problem.
            - assignment_vars: Assignment variables.
        """
        for tutor in self._tutors:
            assigned_topics = [topic[0] for topic in self._topics if topic[0] in tutor[2]]
            prob += (
                lpSum(
                    assignment_vars[(i, topic, tutor[0])]
                    for i in range(1, len(self._groups) + 1)
                    for topic in assigned_topics
                )
                <= tutor[1]["capacity"]
            )

    def _get_results(self, result):
        """
        Returns algorithm results.
        
        Args:
            - result: List of selected variables.
        
        Returns a dictionary that represents the assignment results.
        """
        original_dict = {}
        pattern = re.compile(r"Assignment_(\d+)_(\w+)_(\w+)")
        for var_name in result:
            match = pattern.match(var_name)
            if match:
                i, topic, tutor = match.groups()
                i = int(i)
                if i not in original_dict:
                    original_dict[i] = {}
                original_dict[i][topic] = tutor

        return original_dict
