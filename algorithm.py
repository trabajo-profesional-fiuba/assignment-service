"""Module providing the assignment algorithm that solves the assignment 
of teams to topics and tutors."""

import networkx as nx # pylint: disable=E0401

TEAM_ID = "g"
TOPIC_ID = "t"

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
    result = nx.max_flow_min_cost(graph, "s", "t")
    return result

def is_team_or_topic(string: str, identifier: str):
    """Returns if the string represents a team or a topic."""
    return string.startswith(identifier)

def get_teams_from(result: {}):
    """Returns a dictionary with teams and assigned topic."""
    teams = {}
    for key, value in result.items():
        if is_team_or_topic(key, TEAM_ID):
            for topic, is_assigned in value.items():
                if is_assigned == 1:
                    teams[key] = topic
    return teams

def get_topics_from(result: {}):
    """Returns a dictionary with topics and assigned tutor."""
    topics = {}
    for key, value in result.items():
        if is_team_or_topic(key, TOPIC_ID):
            for tutor, is_assigned in value.items():
                if is_assigned > 0:
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

def show_results(teams: {}, topics: {}):
    """Prints assignment results."""
    for team, topic in teams.items():
        print("Group", team , "has topic" , topic, "and its tutor is", topics[topic]) # pylint: disable=line-too-long

def run_algorithm(edges: []):
    """Runs the assignment algorithm."""
    graph = create_graph(edges)
    result = solve(graph)
    teams, topics, tutors = get_results(result)
    return teams, topics, tutors
