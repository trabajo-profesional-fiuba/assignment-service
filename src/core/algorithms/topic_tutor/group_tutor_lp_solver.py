from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpBinary, PULP_CBC_CMD

from src.constants import GROUP_ID, TOPIC_ID, TUTOR_ID
from src.core.group import UnassignedGroup
from src.core.result import (
    GroupTutorTopicAssignmentResult,
    GroupTutorTopicAssignment,
)
from src.core.topic import Topic
from src.core.tutor import Tutor


class GroupTutorLPSolver:
    def __init__(
        self,
        groups: list[UnassignedGroup],
        topics: list[Topic],
        tutors: list[Tutor],
        balance_limit,
    ):
        """
        Constructor de la clase.

        Args:
            - groups: lista de grupos.
            - tutors: lista de tutores.
            - topics: lista de temas.
            - balance_limit: diferencia máxima entre los grupos asociados a un tutor.

        """
        self._groups = groups
        self._topics = topics
        self._tutors = tutors
        self._balance_limit = balance_limit

    def _create_decision_variables(self) -> dict:
        """
        Crea variables de decisión.

        Itera a través de cada combinación de grupos, temas y tutores,
        creando una variable de decisión binaria para cada combinación.

        Devuelve un diccionario de variables de decisión.
        """
        assignment_vars = {}
        for group in self._groups:
            for tutor in self._tutors:
                for topic in tutor.topics:
                    assignment_vars[(group.id, tutor.id, topic.id)] = LpVariable(
                        f"Assignment-{GROUP_ID}-{group.id}-{TUTOR_ID}-{tutor.id}-{TOPIC_ID}-{topic.id}",
                        0,
                        1,
                        LpBinary,
                    )
        return assignment_vars

    def _create_optimization_problem(self) -> LpProblem:
        """
        Crea el problema de optimización.

        Devuelve una instancia del problema de optimización.
        """
        return LpProblem("GroupAssignment", LpMaximize)

    def _add_objective_function(self, prob: LpProblem, assignment_vars: dict):
        """
        Agrega la función objetivo al problema de optimización.

        Args:
            - prob: Instancia del problema de optimización.
            - assignment_vars: Variables de asignación.

        """
        topic_scores = {
            (group.id, topic.id): 0 for group in self._groups for topic in self._topics
        }

        for group in self._groups:
            # Asignar pesos altos a los temas de preferencia en orden de prioridad
            topic_scores[(group.id, group.topics[0].id)] = 100  # Tema de prioridad 1
            topic_scores[(group.id, group.topics[1].id)] = 90  # Tema de prioridad 2
            topic_scores[(group.id, group.topics[2].id)] = 80  # Tema de prioridad 3

            # Encontrar la categoría que más se repite entre los temas de preferencia
            category_counts = {}
            for topic in group.topics:
                category_counts[topic.category] = (
                    category_counts.get(topic.category, 0) + 1
                )
            most_common_category = max(category_counts, key=category_counts.get)

            # Asignar un peso intermedio a los temas de la categoría más común
            # (excluyendo los ya preferidos)
            for topic in self._topics:
                if topic.category == most_common_category and topic.id not in [
                    t.id for t in group.topics
                ]:
                    topic_scores[(group.id, topic.id)] = (
                        50  # Peso para temas de la categoría más común
                    )

            # Asignar el menor peso a los demás temas
            for topic in self._topics:
                if (
                    topic_scores[(group.id, topic.id)] == 0
                ):  # Si no tiene peso asignado aún
                    topic_scores[(group.id, topic.id)] = (
                        10  # Peso menor para los demás temas
                    )

        # Función objetivo que maximiza la asignación de temas con los pesos
        # establecidos
        prob += lpSum(
            topic_scores[(group.id, topic.id)]
            * assignment_vars[(group.id, tutor.id, topic.id)]
            for group in self._groups
            for tutor in self._tutors
            for topic in tutor.topics
        )

    def _add_constraints(self, prob: LpProblem, assignment_vars: dict):
        """
        Agrega restricciones para el algoritmo de programación lineal.

        Args:
            - prob: Instancia del problema de optimización.
            - assignment_vars: Variables de asignación.
        """
        self._add_group_assignment_constraints(prob, assignment_vars)
        self._add_topic_capacity_constraints(prob, assignment_vars)
        self._add_tutor_capacity_constraints(prob, assignment_vars)
        self._add_balance_constraints(prob, assignment_vars)

    def _add_group_assignment_constraints(self, prob, assignment_vars):
        """
        Agrega restricciones para las asignaciones de grupos.

        Args:
            - prob: Instancia del problema de optimización.
            - assignment_vars: Variables de asignación.
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
        Agrega restricciones para las capacidades de los temas.

        Args:
            - prob: Instancia del problema de optimización.
            - assignment_vars: Variables de asignación.
        """

        for topic in self._topics:
            prob += (
                lpSum(
                    assignment_vars[(group.id, tutor.id, topic.id)]
                    for group in self._groups
                    for tutor in self._tutors
                    if topic.id in tutor.topics_ids()
                )
                <= topic.capacity
            )

    def _add_tutor_capacity_constraints(self, prob, assignment_vars):
        """
        Agrega restricciones para las capacidades de los tutores.

        Args:
            - prob: Instancia del problema de optimización.
            - assignment_vars: Variables de asignación.
        """

        for tutor in self._tutors:
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
        Agrega restricciones para equilibrar el número de grupos asignados a cada tutor.

        Args:
            - prob: Instancia del problema de optimización.
            - assignment_vars: Variables de asignación.
            - max_difference: La diferencia máxima permitida en el número de grupos
            asignados a cualquier par de tutores.
        """

        for tutor_1 in self._tutors:
            for tutor_2 in self._tutors:
                if tutor_1.id != tutor_2.id:
                    prob += (
                        lpSum(
                            assignment_vars[(group.id, tutor_1.id, topic.id)]
                            for group in self._groups
                            for topic in tutor_1.topics
                        )
                        - lpSum(
                            assignment_vars[(group.id, tutor_2.id, topic.id)]
                            for group in self._groups
                            for topic in tutor_2.topics
                        )
                    ) <= self._balance_limit

                    prob += (
                        lpSum(
                            assignment_vars[(group.id, tutor_2.id, topic.id)]
                            for group in self._groups
                            for topic in tutor_2.topics
                        )
                        - lpSum(
                            assignment_vars[(group.id, tutor_1.id, topic.id)]
                            for group in self._groups
                            for topic in tutor_1.topics
                        )
                    ) <= self._balance_limit

    def _solve_optimization_problem(
        self, prob: LpProblem
    ) -> list[GroupTutorTopicAssignment]:
        """
        Resuelve el problema de optimización.

        Args:
            - prob: Instancia del problema de optimización.

        Devuelve una lista de variables seleccionadas y la lista de grupos creados.
        """

        prob.solve(PULP_CBC_CMD(msg=0))

        result = GroupTutorTopicAssignmentResult(status=prob.status, assignments=[])
        if prob.status > 0:
            for var in prob.variables():
                if var.varValue == 1:
                    # Extraer el id del grupo, tutor y topic del nombre de la variable
                    group_id, tutor_id, topic_id = self._parse_variable_name(var.name)

                    # Asignar el tutor al grupo
                    group = self._get_group_by_id(group_id)
                    tutor = self._get_tutor_by_id(tutor_id)

                    topic = self._get_topic_by_id(topic_id)
                    assignment = GroupTutorTopicAssignment(
                        group=group, tutor=tutor, topic=topic
                    )

                    result.add_assignment(assignment)

        return result

    def _parse_variable_name(self, name):
        """
        Analiza el nombre de la variable para extraer el group_id, tutor_id y topic_id.
        Se asume que el formato del nombre de la variable es 'Assignment_group_1_tutor_1_topic_1'.

        Args:
            - name: El nombre de la variable.

        Devuelve una tupla de (group_id, tutor_id, topic_id).
        """

        parts = name.split("_")
        group_id = int(parts[2])
        tutor_id = int(parts[4])
        topic_id = int(parts[6])
        return group_id, tutor_id, topic_id

    def _get_tutor_by_id(self, tutor_id):
        """
        Obtiene la instancia del tutor por su id.

        Args:
            - tutor_id: El id del tutor.

        Devuelve la instancia del tutor.
        """

        return next(tutor for tutor in self._tutors if tutor.id == tutor_id)

    def _get_topic_by_id(self, topic_id):
        """
        Obtiene la lista de temas por sus ids.

        Args:
            - topic_ids: Una lista de ids de temas.

        Devuelve una lista de instancias de Topic.
        """

        return next(topic for topic in self._topics if topic.id == topic_id)

    def _get_group_by_id(self, group_id):
        """
        Obtiene la instancia del grupo por su id.

        Args:
            - group_id: El id del grupo.

        Devuelve la instancia del grupo.
        """

        return next(group for group in self._groups if group.id == group_id)

    def solve(self) -> GroupTutorTopicAssignmentResult:
        """
        Resuelve el problema de optimización utilizando el método de programación lineal.

        Args:
            - groups: lista de grupos.
            - tutors: lista de tutores.
            - topics: lista de temas.

        Devuelve un diccionario que representa el resultado de la asignación.
        """

        assignment_vars = self._create_decision_variables()
        prob = self._create_optimization_problem()
        self._add_objective_function(prob, assignment_vars)
        self._add_constraints(prob, assignment_vars)
        result = self._solve_optimization_problem(prob)
        return result
