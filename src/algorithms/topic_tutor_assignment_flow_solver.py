"""Module providing the assignment algorithm that solves the assignment
of groups to topics and tutors."""

import networkx as nx
from constants import GROUP_ID, TOPIC_ID, SOURCE_NODE_ID, SINK_NODE_ID


class TopicTutorAssignmentFlowSolver:
    def __init__(self, groups: list, topics: list, tutors: list):
        self._groups = groups
        self._topics = topics
        self._tutors = tutors

    def create_source_groups_edges(self):
        """Define edges from source to groups."""
        return [
            (SOURCE_NODE_ID, group.id, {"capacity": 1, "cost": 1})
            for group in self._groups
        ]

    def create_groups_topics_edges(self):
        """Define edges from groups to topics."""
        team_topic_edges = []
        for i, group in enumerate(self._groups):
            for j, topic in enumerate(self._topics):
                team_topic_edges.append(
                    (group.id, topic.id, {"capacity": 1, "weight": group.costs[j]})
                )
        return team_topic_edges

    def create_topics_tutors_edges(self):
        """Define edges from topics to tutors."""
        topic_tutor_edges = []
        for j, tutor in enumerate(self._tutors):
            for k, topic in enumerate(self._topics):
                capacity = tutor.topics["capacities"][k]
                cost = tutor.topics["costs"][k]
                if capacity > 0 and cost > 0:
                    topic_tutor_edges.append(
                        (topic.id, tutor.id, {"capacity": capacity, "weight": cost})
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
        team_topic_edges = self.create_groups_topics_edges()
        source_groups_edges = self.create_source_groups_edges()
        topic_tutor_edges = self.create_topics_tutors_edges()
        tutor_sink_edges = self.create_tutors_sink_edges()
        return (
            team_topic_edges
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

    def is_team_or_topic(self, string: str, identifier: str):
        """Returns if the string represents a team or a topic."""
        return string.startswith(identifier)

    def topic_is_assigned(self, value: bool):
        """Returns if the topic was assigned to the team."""
        return value == 1

    def get_groups_from(self, result: {}):
        """Returns a dictionary with groups and assigned topic."""
        groups = {}
        for key, value in result.items():
            if self.is_team_or_topic(key, GROUP_ID):
                for topic, topic_value in value.items():
                    if self.topic_is_assigned(topic_value):
                        groups[key] = topic
        return groups

    def tutor_is_assigned(self, value: bool):
        """Returns if the tutor was assigned to the topic."""
        return value > 0

    def get_topics_from(self, result: {}):
        """Returns a dictionary with topics and assigned tutor."""
        topics = {}
        for key, value in result.items():
            if self.is_team_or_topic(key, TOPIC_ID):
                for tutor, tutor_value in value.items():
                    if self.tutor_is_assigned(tutor_value):
                        topics[key] = tutor
        return topics

    def get_tutors_from(self, topics: {}, groups: {}):
        """Returns a dictionary with tutors and assigned groups."""
        tutors = {}
        for topic, tutor in topics.items():
            assigned_groups = []
            for team, value in groups.items():
                if value == topic:
                    assigned_groups.append(team)
            tutors[tutor] = assigned_groups
        return tutors

    def get_results(self, result: {}):
        """Returns algorithm results."""
        groups = self.get_groups_from(result)
        topics = self.get_topics_from(result)
        tutors = self.get_tutors_from(topics, groups)
        return groups, topics, tutors

    def solve(self):
        """Runs the assignment algorithm."""
        edges = self.create_edges()
        graph = self.create_graph(edges)
        result = nx.max_flow_min_cost(graph, SOURCE_NODE_ID, SINK_NODE_ID)
        groups, topics, tutors = self.get_results(result)
        return groups, topics, tutors
