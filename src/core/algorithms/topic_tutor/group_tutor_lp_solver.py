from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpBinary, PULP_CBC_CMD

from src.constants import GROUP_ID, TOPIC_ID, TUTOR_ID
from src.core.group import Group
from src.core.group_form_answer import GroupFormAnswer
from src.core.topic import Topic
from src.core.tutor import Tutor


class GroupTutorLPSolver:
    def __init__(self, groups: list[GroupFormAnswer], topics: list[Topic], tutors: list[Tutor], balance_limit):
        """
        Constructor of the class.

        Args:
            - groups: list of groups.
            - tutors: list of tutors.
            - topics: list of topics.
        """
        self._groups = groups
        self._topics = topics
        self._tutors = tutors
        self._balance_limit = balance_limit

    def _create_decision_variables(self):
        """
        Create decision variables.

        It iterates through each combination of groups, topics, and tutors,
        creating a binary decision variable for each combination.

        Returns a dictionary of decision variables.
        """
        assignment_vars = {}
        for group in self._groups:
            for tutor in self._tutors:
                for topic in tutor.topics:
                    assignment_vars[(group.id, tutor.id, topic.id)] = LpVariable(
                        f"Assignment-{GROUP_ID}-{group.id}-{TUTOR_ID}-{tutor.id}-{TOPIC_ID}-{topic.id}", 0, 1, LpBinary
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
            (group.id, topic.id): 0
            for group in self._groups
            for topic in self._topics
        }

        for group in self._groups:
            # Asignar pesos altos a los temas de preferencia en orden de prioridad
            topic_scores[(group.id, group.topics[0].id)] = 100  # Tema de prioridad 1
            topic_scores[(group.id, group.topics[1].id)] = 90   # Tema de prioridad 2
            topic_scores[(group.id, group.topics[2].id)] = 80   # Tema de prioridad 3

            # Encontrar la categoría que más se repite entre los temas de preferencia
            category_counts = {}
            for topic in group.topics:
                category_counts[topic.category] = category_counts.get(topic.category, 0) + 1
            most_common_category = max(category_counts, key=category_counts.get)

            # Asignar un peso intermedio a los temas de la categoría más común (excluyendo los ya preferidos)
            for topic in self._topics:
                if topic.category == most_common_category and topic.id not in [t.id for t in group.topics]:
                    topic_scores[(group.id, topic.id)] = 50  # Peso para temas de la categoría más común

            # Asignar el menor peso a los demás temas
            for topic in self._topics:
                if topic_scores[(group.id, topic.id)] == 0:  # Si no tiene peso asignado aún
                    topic_scores[(group.id, topic.id)] = 10  # Peso menor para los demás temas

        # Función objetivo que maximiza la asignación de temas con los pesos establecidos
        prob += lpSum(
            topic_scores[(group.id, topic.id)] * assignment_vars[(group.id, tutor.id, topic.id)]
            for group in self._groups
            for tutor in self._tutors
            for topic in tutor.topics
        )

    def _add_constraints(self, prob, assignment_vars):
        """
        Add constraints for the linear programming algorithm.

        Args:
            - prob: Instance of the optimization problem.
            - assignment_vars: Assignment variables.
        """
        self._add_group_assignment_constraints(prob, assignment_vars)
        self._add_topic_capacity_constraints(prob, assignment_vars)
        self._add_tutor_capacity_constraints(prob, assignment_vars)
        self._add_balance_constraints(prob, assignment_vars)

    def _add_group_assignment_constraints(self, prob, assignment_vars):
        """
        Add constraints for group assignments.

        Args:
            - prob: Instance of the optimization problem.
            - assignment_vars: Assignment variables.
        """
        for group in self._groups:
            prob += (
                lpSum(
                    assignment_vars[(group.id, tutor.id, topic.id)]
                    for tutor in self._tutors
                    for topic in tutor.topics
                )
                == 1
            )

    def _add_topic_capacity_constraints(self, prob, assignment_vars):
        """
        Add constraints for topic capacities.

        Args:
            - prob: Instance of the optimization problem.
            - assignment_vars: Assignment variables.
        """

        for topic in self._topics:
            prob += lpSum(
                assignment_vars[(group.id, tutor.id, topic.id)]
                for group in self._groups
                for tutor in self._tutors
                if topic.id in tutor.topics_ids()
            ) <= topic.capacity

    def _add_tutor_capacity_constraints(self, prob, assignment_vars):
        """
        Add constraints for tutor capacities.

        Args:
            - prob: Instance of the optimization problem.
            - assignment_vars: Assignment variables.
        """
        for tutor in self._tutors:
            print(tutor.capacity)
            assigned_topics = [topic.id for topic in tutor.topics]
            prob += (
                lpSum(
                    assignment_vars[(group.id, tutor.id, topic)]
                    for group in self._groups
                    for topic in assigned_topics
                )
                <= tutor.capacity
            )

    def _add_balance_constraints(self, prob, assignment_vars):
        """
        Add constraints to balance the number of groups assigned to each tutor.

        Args:
            - prob: Instance of the optimization problem.
            - assignment_vars: Assignment variables.
            - max_difference: The maximum allowed difference in the number of groups assigned to any two tutors.
        """
        for tutor_1 in self._tutors:
            for tutor_2 in self._tutors:
                if tutor_1.id != tutor_2.id:
                    prob += (
                        lpSum(assignment_vars[(group.id, tutor_1.id, topic.id)]
                            for group in self._groups
                            for topic in tutor_1.topics) 
                        -
                        lpSum(assignment_vars[(group.id, tutor_2.id, topic.id)]
                            for group in self._groups
                            for topic in tutor_2.topics)
                    ) <= self._balance_limit

                    prob += (
                        lpSum(assignment_vars[(group.id, tutor_2.id, topic.id)]
                            for group in self._groups
                            for topic in tutor_2.topics) 
                        -
                        lpSum(assignment_vars[(group.id, tutor_1.id, topic.id)]
                            for group in self._groups
                            for topic in tutor_1.topics)
                    ) <= self._balance_limit


    def _solve_optimization_problem(self, prob):
        """
        Solve the optimization problem.

        Args:
            - prob: Instance of the optimization problem.

        Returns a list of selected variables and the list of created groups.
        """
        prob.solve(PULP_CBC_CMD(msg=0))

        result_variables = []
        groups_result = []
        
        for var in prob.variables():
            print(var.name, var.varValue)
            if var.varValue == 1:
                print(var)
                result_variables.append(var)

                # Extraer el id del grupo, tutor y topic del nombre de la variable 
                group_id, tutor_id, topic_id = self._parse_variable_name(var.name)
                
                # Crear el grupo con el id correspondiente
                group = Group(id=group_id)
                
                # Asignar el tutor al grupo
                tutor = self._get_tutor_by_id(tutor_id)
                group.assign_tutor(tutor)
                
                # Asignar el topic al grupo
                topic = self._get_topic_by_id(topic_id)
                group.assign_topic(topic)
                
                groups_result.append(group)

        return groups_result

    def _parse_variable_name(self, name):
        """
        Parse the variable name to extract the group_id, tutor_id, and topic_id.
        Assumes the format of the variable name is 'Assignment_group_1_tutor_1_topic_1'.

        Args:
            - name: The name of the variable.

        Returns a tuple of (group_id, tutor_id, topic_id).
        """
        parts = name.split('_')
        group_id = int(parts[2])  
        tutor_id = int(parts[4])  
        topic_id = int(parts[6])  
        return group_id, tutor_id, topic_id

    def _get_tutor_by_id(self, tutor_id):
        """
        Get the tutor instance by its id.

        Args:
            - tutor_id: The id of the tutor.

        Returns the tutor instance.
        """
        return next(tutor for tutor in self._tutors if tutor.id == tutor_id)

    def _get_topic_by_id(self, topic_id):
        """
        Get the list of topics by their ids.

        Args:
            - topic_ids: A list of topic ids.

        Returns a list of Topic instances.
        """
        for topic in self._topics:
            if topic.id == topic_id:
                return topic

    def solve(self):
        """
        Solve the optimization problem using the linear programming method.

        Args:
            - groups: list of groups.
            - tutors: list of tutors.
            - topics: list of topics.

        Returns a dictionary that represents the result of the assignment.
        """
        assignment_vars = self._create_decision_variables()
        prob = self._create_optimization_problem()
        self._add_objective_function(prob, assignment_vars)
        self._add_constraints(prob, assignment_vars)
        result = self._solve_optimization_problem(prob)
        return result
