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
    teams = []
    for key, value in result.items():
        if key.startswith("g"):
            for k, v in value.items():
                if v == 1:
                    teams.append([key,k])
    return teams

def get_topics_and_tutors_from(result):
    """Returns topics results."""
    topics_and_tutors = []
    for key, value in result.items():
        if key.startswith("t"):
            for k,v in value.items():
                if v >= 1:
                    topics_and_tutors.append([key,k])
    return topics_and_tutors

def show_results(teams: [], topics_and_tutors: []):
    """Prints assignment results."""
    for team in teams:
        a = team[0]
        for topic_and_tutor in topics_and_tutors:
            if topic_and_tutor[0] == team[1]:
                print("Group", a , "has topic " , topic_and_tutor[0], "and its tutor is:", topic_and_tutor[1]) # pylint: disable=line-too-long

def run_algorithm(edges: []):
    """Runs the assignment algorithm."""
    graph = create_graph(edges)
    result = solve(graph)
    teams = get_teams_from(result)
    topics_and_tutors = get_topics_and_tutors_from(result)
    show_results(teams, topics_and_tutors)

# Edges from groups nodes to topics nodes
group1_t1 = ("g1", "t1", {"capacity": 1, "weight": 1})
group1_t2 = ("g1", "t2", {"capacity": 1, "weight": 2})
group1_t3 = ("g1", "t3", {"capacity": 1, "weight": 3})
group1_t4 = ("g1", "t4", {"capacity": 1, "weight": 4})
group1_t5 = ("g1", "t5", {"capacity": 1, "weight": 4})
group1_t6 = ("g1", "t6", {"capacity": 1, "weight": 4})

group2_t1 = ("g2", "t1", {"capacity": 1, "weight": 4})
group2_t2 = ("g2", "t2", {"capacity": 1, "weight": 4})
group2_t3 = ("g2", "t3", {"capacity": 1, "weight": 4})
group2_t4 = ("g2", "t4", {"capacity": 1, "weight": 1})
group2_t5 = ("g2", "t5", {"capacity": 1, "weight": 2})
group2_t6 = ("g2", "t6", {"capacity": 1, "weight": 3})

group3_t1 = ("g3", "t1", {"capacity": 1, "weight": 1})
group3_t2 = ("g3", "t2", {"capacity": 1, "weight": 4})
group3_t3 = ("g3", "t3", {"capacity": 1, "weight": 2})
group3_t4 = ("g3", "t4", {"capacity": 1, "weight": 4})
group3_t5 = ("g3", "t5", {"capacity": 1, "weight": 3})
group3_t6 = ("g3", "t6", {"capacity": 1, "weight": 4})

# Edges from source node (s) to groups nodes
s_group1 = ("s", "g1", {"capacity": 1, "weight": 1})
s_group2 = ("s", "g2", {"capacity": 1, "weight": 1})
s_group3 = ("s", "g3", {"capacity": 1, "weight": 1})

# Edges from topics nodes to tutors nodes
t1_p1 = ("t1", "p1", {"capacity": 3, "weight": 1})
t2_p1 = ("t2", "p1", {"capacity": 3, "weight": 1})
t3_p2 = ("t3", "p2", {"capacity": 3, "weight": 1})
t4_p2 = ("t4", "p2", {"capacity": 3, "weight": 1})
t5_p2 = ("t5", "p2", {"capacity": 3, "weight": 1})
t6_p2 = ("t6", "p2", {"capacity": 3, "weight": 1})

# Edges from tutors nodes to sink node (t)
p1_t = ("p1", "t", {"capacity": 3, "weight": 1})
p2_t = ("p2", "t", {"capacity": 2, "weight": 1})

example_edges = [group1_t1,group1_t2,group1_t3,group1_t4,group1_t5,group1_t6,
           group2_t1,group2_t2,group2_t3,group2_t4,group2_t5,group2_t6,
           group3_t1,group3_t2,group3_t3,group3_t4,group3_t5,group3_t6,
           s_group1,s_group2,s_group3,
           t1_p1,t2_p1,t3_p2,t4_p2,t5_p2,t6_p2,
           p1_t,p2_t]

run_algorithm(example_edges)
