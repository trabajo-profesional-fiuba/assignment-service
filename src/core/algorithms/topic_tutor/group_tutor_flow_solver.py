"""
Module providing the assignment flow algorithm that solves the assignment
of groups to topics and tutors.
"""

from typing import Optional
import networkx as nx

from src.constants import SOURCE_NODE_ID, SINK_NODE_ID, GROUP_ID, TOPIC_ID, TUTOR_ID
from src.core.group import UnassignedGroup
from src.core.result import GroupTutorTopicAssignmentResult, GroupTutorTopicAssignment
from src.core.topic import Topic
from src.core.tutor import Tutor


class GroupTutorFlowSolver:
    """
    A solver for assigning groups to topics and tutors using a flow-based algorithm.
    """

    def __init__(
        self,
        groups: Optional[list[UnassignedGroup]] = None,
        topics: Optional[list[Topic]] = None,
        tutors: Optional[list[Tutor]] = None,
    ):
        """
        Inicializa el solucionador con los grupos, temas y tutores proporcionados.

        Attributes:
            groups (list[Group]): Una lista de objetos de grupo que se van a asignar.
            tutors (list[Tutor]): Una lista de objetos de tutor que se van a asignar a
            temas.
        """

        self._groups = groups if groups is not None else []
        self._tutors = tutors if tutors is not None else []
        self._topics = topics if topics is not None else []

    def _create_source_groups_edges(self) -> list[tuple[str, str, dict[str, int]]]:
        """
        Define las aristas desde el nodo fuente hasta los nodos de grupo.

        Returns:
            list[tuple[str, str, dict[str, int]]]: Una lista de aristas con capacidades
            y costos.
        """

        return [
            (SOURCE_NODE_ID, f"{GROUP_ID}-{group.id}", {"capacity": 1, "cost": 1})
            for group in self._groups
        ]

    def _create_groups_topics_edges(self) -> list[tuple[str, str, dict[str, int]]]:
        """
        Define las aristas desde los nodos de grupo hasta los nodos de tema.

        Returns:
            list[tuple[str, str, dict[str, int]]]: Una lista de aristas con capacidades
            y costos.
        """

        group_topic_edges = []

        for group in self._groups:
            for topic in self._topics:
                topic_id = topic.id
                group_topic_edges.append(
                    (
                        f"{GROUP_ID}-{group.id}",
                        f"{TOPIC_ID}-{topic_id}",
                        {
                            "capacity": 1,
                            "cost": group.preference_of(topic),
                        },
                    )
                )
        return group_topic_edges

    def _create_topics_tutors_edges(self) -> list[tuple[str, str, dict[str, int]]]:
        """
        Define las aristas desde los nodos de tema hasta los nodos de tutor.

        Returns:
            list[tuple[str, str, dict[str, int]]]: Una lista de aristas con capacidades
            y costos.
        """

        topic_tutor_edges = []
        for tutor in self._tutors:
            for topic in self._topics:
                capacity = tutor.capacity_of(topic)
                if capacity > 0:
                    topic_tutor_edges.append(
                        (
                            f"{TOPIC_ID}-{topic.id}",
                            f"{TUTOR_ID}-{tutor.id}",
                            {
                                "capacity": capacity,
                                "cost": 1,
                            },
                        )
                    )
        return topic_tutor_edges

    def _create_tutors_sink_edges(self) -> list[tuple[str, str, dict[str, int]]]:
        """
        Define las aristas desde los nodos de tutor hasta el nodo sumidero.

        Returns:
            list[tuple[str, str, dict[str, int]]]: Una lista de aristas con capacidades
            y costos.
        """

        tutor_sink_edges = [
            (
                f"{TUTOR_ID}-{tutor.id}",
                SINK_NODE_ID,
                {"capacity": tutor.capacity, "cost": 1},
            )
            for tutor in self._tutors
        ]
        return tutor_sink_edges

    def _create_edges(self) -> list[tuple[str, str, dict[str, int]]]:
        """
        Crea todas las aristas necesarias para construir el digrafo.

        Las aristas conectan el nodo fuente a los nodos de grupo, los nodos de grupo a los nodos de tema,
        los nodos de tema a los nodos de tutor y los nodos de tutor al nodo sumidero.

        Returns:
            list[tuple[str, str, dict[str, int]]]: Una lista de todas las aristas en el grafo.
        """

        source_groups_edges = self._create_source_groups_edges()
        group_topic_edges = self._create_groups_topics_edges()
        topic_tutor_edges = self._create_topics_tutors_edges()
        tutor_sink_edges = self._create_tutors_sink_edges()
        return (
            group_topic_edges
            + source_groups_edges
            + topic_tutor_edges
            + tutor_sink_edges
        )

    def _create_graph(self, edges: list[tuple[str, str, dict[str, int]]]) -> nx.DiGraph:
        """
        Crea un grafo dirigido (digrafo) con las aristas dadas, incluyendo costos
        y capacidades.

        Args:
            edges (list[tuple[str, str, dict[str, int]]]): Las aristas a agregar al
            grafo.

        Returns:
            nx.DiGraph: El grafo dirigido creado.
        """

        graph = nx.DiGraph()
        graph.add_edges_from(edges)
        return graph

    def _convert_result(self, graph: nx.DiGraph, result: dict):
        if sum(result[SOURCE_NODE_ID].values()) == len(self._groups):
            assigment_result = GroupTutorTopicAssignmentResult(status=1, assignments=[])
            group_ids = list()
            for key in result[SOURCE_NODE_ID].keys():
                group_id = key.split("-")[1]
                group_ids.append(int(group_id))

            for i in group_ids:
                path = nx.shortest_path(graph, f"{GROUP_ID}-{i}", f"{SINK_NODE_ID}")
                _, topic_id, tutor_id, _ = path
                topic = next(
                    (t for t in self._topics if t.id == int(topic_id.split("-")[1])),
                    None,
                )
                tutor = next(
                    (t for t in self._tutors if t.id == int(tutor_id.split("-")[1])),
                    None,
                )
                group = next((g for g in self._groups if g.id == i), None)
                assigment_result.add_assignment(
                    GroupTutorTopicAssignment(group=group, tutor=tutor, topic=topic)
                )
        else:
            assigment_result = GroupTutorTopicAssignmentResult(
                status=-1, assignments=[]
            )

        return assigment_result

    def solve(self) -> GroupTutorTopicAssignmentResult:
        """
        Ejecuta el algoritmo de asignación para encontrar el flujo máximo de
        costo mínimo.

        El algoritmo asigna grupos a temas y temas a tutores,
        luego calcula el flujo óptimo desde el nodo fuente hasta el nodo sumidero.

        Returns:
            dict[str, dict[str, int]]: Un diccionario que representa el flujo
            desde cada nodo a sus nodos conectados.
        """

        edges = self._create_edges()
        graph = self._create_graph(edges)
        result = nx.max_flow_min_cost(
            graph, SOURCE_NODE_ID, SINK_NODE_ID, capacity="capacity", weight="cost"
        )
        group_tutor_assigment_results = self._convert_result(graph, result)
        return group_tutor_assigment_results
