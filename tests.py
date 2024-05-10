from algorithm import run_algorithm

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
