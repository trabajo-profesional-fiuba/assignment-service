"""Module providing the assignment algorithm that solves the assignment
of groups to topics and tutors."""

import networkx as nx
from src.constants import SOURCE_NODE_ID, SINK_NODE_ID


class TopicTutorAssignmentFlowSolver:
    def __init__(self, groups: list, topics: list, tutors: list):
        self._groups = groups
        self._topics = topics
        self._tutors = tutors

    def create_source_groups_edges(self):
        """Define edges from source to groups."""
        return [
            (SOURCE_NODE_ID, group.id, {"capacity": 1, "weight": 1})
            for group in self._groups
        ]

    def create_groups_topics_edges(self):
        """Define edges from groups to topics."""
        group_topic_edges = []
        for i, group in enumerate(self._groups):
            for j, topic in enumerate(self._topics):
                group_topic_edges.append(
                    (
                        group.id,
                        topic.id,
                        {
                            "capacity": 1,
                            "weight": group.cost_of(topic),
                        },
                    )
                )
        return group_topic_edges

    def create_topics_tutors_edges(self):
        """Define edges from topics to tutors."""
        topic_tutor_edges = []
        for j, tutor in enumerate(self._tutors):
            for k, topic in enumerate(self._topics):
                topic_tutor_edges.append(
                    (
                        topic.id,
                        tutor.id,
                        {
                            "capacity": tutor.capacity_of(topic),
                            "weight": tutor.cost_of(topic),
                        },
                    )
                )
        return topic_tutor_edges

    def create_tutors_sink_edges(self):
        """Define edges from tutors to sink."""
        tutor_sink_edges = [
            (tutor.id, SINK_NODE_ID, {"capacity": tutor.capacity, "weight": 1})
            for i, tutor in enumerate(self._tutors)
        ]
        return tutor_sink_edges

    def create_edges(self):
        """Creates edges to create a digraph.
        The edges are from source node to groups nodes, from groups
        nodes to topic nodes, from topics nodes to tutors nodes, and
        from tutors nodes to sink node."""
        group_topic_edges = self.create_groups_topics_edges()
        source_groups_edges = self.create_source_groups_edges()
        topic_tutor_edges = self.create_topics_tutors_edges()
        tutor_sink_edges = self.create_tutors_sink_edges()
        return (
            group_topic_edges
            + source_groups_edges
            + topic_tutor_edges
            + tutor_sink_edges
        )

    def create_graph(self, edges: []):
        """Creates a digraph with edge costs and capacities.
        There is a source node s and a sink node t."""
        graph = nx.DiGraph()
        graph.add_edges_from(edges)
        return graph

    def solve(self):
        """Runs the assignment algorithm."""
        edges = self.create_edges()
        graph = self.create_graph(edges)
        flow_dict = nx.max_flow_min_cost(graph, SOURCE_NODE_ID, SINK_NODE_ID)
        return flow_dict
