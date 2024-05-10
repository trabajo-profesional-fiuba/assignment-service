"""Module providing the assignment algorithm that solves the assignment 
of teams to topics and tutors."""

# pylint: disable=E0401
import networkx as nx

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

def get_teams_from(result: {}):
    """Returns teams results."""
    teams = {}
    for key, value in result.items():
        if key.startswith("g"):
            for topic, is_assigned in value.items():
                if is_assigned == 1:
                    teams[key] = topic
    return teams

def get_topics_from(result):
    """Returns topics results."""
    topics = {}
    for key, value in result.items():
        if key.startswith("t"):
            for tutor, value in value.items():
                if value > 0:
                    topics[key] = tutor
    return topics

def show_results(teams: {}, topics: {}):
    """Prints assignment results."""
    for team, topic in teams.items():
        print("Group", team , "has topic " , topic, "and its tutor is:", topics[topic]) # pylint: disable=line-too-long

def run_algorithm(edges: []):
    """Runs the assignment algorithm."""
    graph = create_graph(edges)
    result = solve(graph)
    teams = get_teams_from(result)
    topics_and_tutors = get_topics_from(result)
    show_results(teams, topics_and_tutors)
