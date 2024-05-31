"""
Module providing the assignment flow algorithm that solves the assignment
of groups to topics and tutors.
"""

import networkx as nx
from typing import List, Dict, Tuple
from src.constants import SOURCE_NODE_ID, SINK_NODE_ID
from src.model.group.initial_state_group import InitialStateGroup
from src.model.topic import Topic
from src.model.tutor.initial_state_tutor import InitialStateTutor


class TopicTutorAssignmentFlowSolver:
    """
    A solver for assigning groups to topics and tutors using a flow-based algorithm.

    Attributes:
        groups (List[InitialStateGroup]): A list of group objects to be assigned.
        topics (List[Topic]): A list of topic objects to be assigned to groups.
        tutors (List[InitialStateTutor]): A list of tutor objects to be assigned to
        topics.
    """

    def __init__(
        self,
        groups: List[InitialStateGroup],
        topics: List[Topic],
        tutors: List[InitialStateTutor],
    ) -> None:
        """
        Initializes the solver with the provided groups, topics, and tutors.

        Args:
            groups (List[InitialStateGroup]): The groups to be assigned.
            topics (List[Topic]): The topics to be assigned to groups.
            tutors (List[InitialStateTutor]): The tutors to be assigned to topics.
        """
        self._groups = groups
        self._topics = topics
        self._tutors = tutors

    def _create_source_groups_edges(self) -> List[Tuple[str, str, Dict[str, int]]]:
        """
        Defines edges from the source node to group nodes.

        Returns:
            List[Tuple[str, str, Dict[str, int]]]: A list of edges with capacities
            and costs.
        """
        return [
            (SOURCE_NODE_ID, group.id, {"capacity": 1, "cost": 1})
            for group in self._groups
        ]

    def _create_groups_topics_edges(self) -> List[Tuple[str, str, Dict[str, int]]]:
        """
        Defines edges from group nodes to topic nodes.

        Returns:
            List[Tuple[str, str, Dict[str, int]]]: A list of edges with capacities
            and costs.
        """
        group_topic_edges = []
        for i, group in enumerate(self._groups):
            for j, topic in enumerate(self._topics):
                group_topic_edges.append(
                    (
                        group.id,
                        topic.id,
                        {
                            "capacity": 1,
                            "cost": group.cost_of(topic),
                        },
                    )
                )
        return group_topic_edges

    def _create_topics_tutors_edges(self) -> List[Tuple[str, str, Dict[str, int]]]:
        """
        Defines edges from topic nodes to tutor nodes.

        Returns:
            List[Tuple[str, str, Dict[str, int]]]: A list of edges with capacities
            and costs.
        """
        topic_tutor_edges = []
        for j, tutor in enumerate(self._tutors):
            for k, topic in enumerate(self._topics):
                topic_tutor_edges.append(
                    (
                        topic.id,
                        tutor.id,
                        {
                            "capacity": tutor.capacity_of(topic),
                            "cost": tutor.cost_of(topic),
                        },
                    )
                )
        return topic_tutor_edges

    def _create_tutors_sink_edges(self) -> List[Tuple[str, str, Dict[str, int]]]:
        """
        Defines edges from tutor nodes to the sink node.

        Returns:
            List[Tuple[str, str, Dict[str, int]]]: A list of edges with capacities
            and costs.
        """
        tutor_sink_edges = [
            (tutor.id, SINK_NODE_ID, {"capacity": tutor.capacity, "cost": 1})
            for i, tutor in enumerate(self._tutors)
        ]
        return tutor_sink_edges

    def _create_edges(self) -> List[Tuple[str, str, Dict[str, int]]]:
        """
        Creates all the edges needed to construct the digraph.

        The edges connect the source node to group nodes, group nodes to topic nodes,
        topic nodes to tutor nodes, and tutor nodes to the sink node.

        Returns:
            List[Tuple[str, str, Dict[str, int]]]: A list of all edges in the graph.
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

    def _create_graph(self, edges: List[Tuple[str, str, Dict[str, int]]]) -> nx.DiGraph:
        """
        Creates a directed graph (digraph) with the given edges, including costs
        and capacities.

        Args:
            edges (List[Tuple[str, str, Dict[str, int]]]): The edges to add to
            the graph.

        Returns:
            nx.DiGraph: The created directed graph.
        """
        graph = nx.DiGraph()
        graph.add_edges_from(edges)
        return graph

    def solve(self) -> Dict[str, Dict[str, int]]:
        """
        Runs the assignment algorithm to find the maximum flow of
        minimum cost.

        The algorithm assigns groups to topics and topics to tutors,
        then computes the optimal flow from the source node to the sink node.

        Returns:
            Dict[str, Dict[str, int]]: A dictionary representing the flow
            from each node to its connected nodes.
        """
        edges = self._create_edges()
        graph = self._create_graph(edges)
        flow_dict = nx.max_flow_min_cost(
            graph, SOURCE_NODE_ID, SINK_NODE_ID, capacity="capacity", weight="cost"
        )
        return flow_dict
