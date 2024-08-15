"""
Module providing the assignment flow algorithm that solves the assignment
of groups to topics and tutors.
"""

import networkx as nx

from src.constants import SOURCE_NODE_ID, SINK_NODE_ID, GROUP_ID, TOPIC_ID, TUTOR_ID
from src.core.group import Group
from src.core.tutor import Tutor


class GroupTutorFlowSolver:
    """
    A solver for assigning groups to topics and tutors using a flow-based algorithm.
    """

    def __init__(
        self,
        groups: list[Group],
        tutors: list[Tutor],
    ) -> None:
        """
        Initializes the solver with the provided groups, topics, and tutors.

        Attributes:
            groups (list[Group]): A list of group objects to be assigned.
            tutors (list[Tutor]): A list of tutor objects to be assigned to
            topics.
        """
        self._groups = groups
        self._tutors = tutors

    def _create_source_groups_edges(self) -> list[tuple[str, str, dict[str, int]]]:
        """
        Defines edges from the source node to group nodes.

        Returns:
            list[tuple[str, str, dict[str, int]]]: A list of edges with capacities
            and costs.
        """
        return [
            (SOURCE_NODE_ID, f"{GROUP_ID}-{group.id}", {"capacity": 1, "cost": 1})
            for group in self._groups
        ]

    def _create_groups_topics_edges(self) -> list[tuple[str, str, dict[str, int]]]:
        """
        Defines edges from group nodes to topic nodes.

        Returns:
            list[tuple[str, str, dict[str, int]]]: A list of edges with capacities
            and costs.
        """
        group_topic_edges = []
        for i, group in enumerate(self._groups):
            for j, topic in enumerate(group.topics):
                group_topic_edges.append(
                    (
                        f"{GROUP_ID}-{group.id}",
                        f"{TOPIC_ID}-{topic.id}",
                        {
                            "capacity": 1,
                            "cost": group.preference_of(topic),
                        },
                    )
                )
        return group_topic_edges

    def _create_topics_tutors_edges(self) -> list[tuple[str, str, dict[str, int]]]:
        """
        Defines edges from topic nodes to tutor nodes.

        Returns:
            list[tuple[str, str, dict[str, int]]]: A list of edges with capacities
            and costs.
        """
        topic_tutor_edges = []
        for j, tutor in enumerate(self._tutors):
            for k, topic in enumerate(tutor.topics()):
                topic_tutor_edges.append(
                    (
                        f"{TOPIC_ID}-{topic.id}",
                        f"{TUTOR_ID}-{tutor.id}",
                        {
                            "capacity": tutor.capacity_of(topic),
                            "cost": tutor.preference_of(topic),
                        },
                    )
                )
        return topic_tutor_edges

    def _create_tutors_sink_edges(self) -> list[tuple[str, str, dict[str, int]]]:
        """
        Defines edges from tutor nodes to the sink node.

        Returns:
            list[tuple[str, str, dict[str, int]]]: A list of edges with capacities
            and costs.
        """
        tutor_sink_edges = [
            (
                f"{TUTOR_ID}-{tutor.id}",
                SINK_NODE_ID,
                {"capacity": tutor.capacity(), "cost": 1},
            )
            for i, tutor in enumerate(self._tutors)
        ]
        return tutor_sink_edges

    def _create_edges(self) -> list[tuple[str, str, dict[str, int]]]:
        """
        Creates all the edges needed to construct the digraph.

        The edges connect the source node to group nodes, group nodes to topic nodes,
        topic nodes to tutor nodes, and tutor nodes to the sink node.

        Returns:
            list[tuple[str, str, dict[str, int]]]: A list of all edges in the graph.
        """
        group_topic_edges = self._create_groups_topics_edges()
        source_groups_edges = self._create_source_groups_edges()
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
        Creates a directed graph (digraph) with the given edges, including costs
        and capacities.

        Args:
            edges (list[tuple[str, str, dict[str, int]]]): The edges to add to
            the graph.

        Returns:
            nx.DiGraph: The created directed graph.
        """
        graph = nx.DiGraph()
        graph.add_edges_from(edges)
        return graph

    def solve(self) -> dict[str, dict[str, int]]:
        """
        Runs the assignment algorithm to find the maximum flow of
        minimum cost.

        The algorithm assigns groups to topics and topics to tutors,
        then computes the optimal flow from the source node to the sink node.

        Returns:
            dict[str, dict[str, int]]: A dictionary representing the flow
            from each node to its connected nodes.
        """
        edges = self._create_edges()
        graph = self._create_graph(edges)
        flow_dict = nx.max_flow_min_cost(
            graph, SOURCE_NODE_ID, SINK_NODE_ID, capacity="capacity", weight="cost"
        )
        return flow_dict
