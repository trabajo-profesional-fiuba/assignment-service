"""Module providing the assignment algorithm that solves the assignment
of teams to topics and tutors."""

import networkx as nx
from constants import TEAM_ID, TOPIC_ID, SOURCE_NODE_ID, SINK_NODE_ID


def create_graph(edges: []):
    """Creates a digraph with edge costs and capacities.
    There is a source node s and a sink node t."""
    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    return graph


def solve(graph: nx.DiGraph):
    """Finds a maximum flow from s to t whose total cost is minimized.
    Returns a dictionary of dictionaries keyed by nodes such that flowDict[u][v]
    is the flow edge (u, v)."""
    result = nx.max_flow_min_cost(graph, SOURCE_NODE_ID, SINK_NODE_ID)
    return result


def is_team_or_topic(string: str, identifier: str):
    """Returns if the string represents a team or a topic."""
    return string.startswith(identifier)


def topic_is_assigned(value: bool):
    """Returns if the topic was assigned to the team."""
    return value == 1


def get_teams_from(result: {}):
    """Returns a dictionary with teams and assigned topic."""
    teams = {}
    for key, value in result.items():
        if is_team_or_topic(key, TEAM_ID):
            for topic, topic_value in value.items():
                if topic_is_assigned(topic_value):
                    teams[key] = topic
    return teams


def tutor_is_assigned(value: bool):
    """Returns if the tutor was assigned to the topic."""
    return value > 0


def get_topics_from(result: {}):
    """Returns a dictionary with topics and assigned tutor."""
    topics = {}
    for key, value in result.items():
        if is_team_or_topic(key, TOPIC_ID):
            for tutor, tutor_value in value.items():
                if tutor_is_assigned(tutor_value):
                    topics[key] = tutor
    return topics


def get_tutors_from(topics: {}, teams: {}):
    """Returns a dictionary with tutors and assigned teams."""
    tutors = {}
    for topic, tutor in topics.items():
        assigned_teams = []
        for team, value in teams.items():
            if value == topic:
                assigned_teams.append(team)
        tutors[tutor] = assigned_teams
    return tutors


def get_results(result: {}):
    """Returns algorithm results."""
    teams = get_teams_from(result)
    topics = get_topics_from(result)
    tutors = get_tutors_from(topics, teams)
    return teams, topics, tutors


def max_flow_min_cost(edges: []):
    """Runs the assignment algorithm."""
    graph = create_graph(edges)
    result = solve(graph)
    teams, topics, tutors = get_results(result)
    return teams, topics, tutors
