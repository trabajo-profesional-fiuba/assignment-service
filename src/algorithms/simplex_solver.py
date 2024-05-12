from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpBinary, LpStatus

def assign_groups_lp(groups, professors, topics):
    # Create the optimization problem
    prob = _create_optimization_problem(groups, professors, topics)

    # Add the objective function to maximize
    _add_objective_function(prob, groups, professors, topics)

    # Add constraints for group assignments
    _add_group_assignment_constraints(prob, groups, professors, topics)

    # Add constraints for topic capacities
    _add_topic_capacity_constraints(prob, groups, professors, topics)

    # Add constraints for professor capacities
    _add_professor_capacity_constraints(prob, groups, professors, topics)

    # Solve the optimization problem
    _solve_optimization_problem(prob)

def _create_optimization_problem(groups, professors, topics):
    return LpProblem("Group Assignment", LpMaximize)

def _add_objective_function(prob, groups, professors, topics):
    assignment_vars = _create_decision_variables(groups, professors, topics)
    topic_scores = _calculate_topic_scores(groups, topics)
    prob += lpSum(topic_scores[(i, topic['topic'])] * assignment_vars[(i, topic['topic'], professor['name'])] for i in range(1, len(groups)+1) for topic in topics for professor in professors if topic['topic'] in professor['topics'])

def _create_decision_variables(groups, professors, topics):
    return LpVariable.dicts(
        "Assignment",
         [(i, topic['topic'], professor['name']) for i in range(1, len(groups)+1) for topic in topics for professor in professors if topic['topic'] in professor['topics']],
         0, 1, LpBinary)

def _calculate_topic_scores(groups, topics):
    topic_scores = {(i, topic['topic']): 0 for i in range(1, len(groups)+1) for topic in topics}
    for i, group in enumerate(groups, 1):
        for j, topic in enumerate(group):
            topic_scores[(i, topic)] = len(group) - j
    return topic_scores

def _add_group_assignment_constraints(prob, groups, professors, topics):
    assignment_vars = _create_decision_variables(groups, professors, topics)
    for i, group in enumerate(groups, 1):
        prob += lpSum(assignment_vars[(i, topic, professor['name'])] for topic in group for professor in professors if topic in professor['topics']) == 1

def _add_topic_capacity_constraints(prob, groups, professors, topics):
    assignment_vars = _create_decision_variables(groups, professors, topics)
    for topic in topics:
        prob += lpSum(assignment_vars[(i, topic['topic'], professor['name'])] for i in range(1, len(groups)+1) for professor in professors if topic['topic'] in professor['topics']) <= topic['capacity']

def _add_professor_capacity_constraints(prob, groups, professors, topics):
    assignment_vars = _create_decision_variables(groups, professors, topics)
    for professor in professors:
        assigned_topics = [topic['topic'] for topic in topics if topic['topic'] in professor['topics']]
        prob += lpSum(assignment_vars[(i, topic, professor['name'])] for i in range(1, len(groups)+1) for topic in assigned_topics) <= professor['capacity']

def _solve_optimization_problem(prob):
    prob.solve()
    print("Status:", LpStatus[prob.status])
    _show_decision_variables(prob)

def _show_decision_variables(prob):
    print("Decision variables with value 1:")
    for var in prob.variables():
        if var.varValue == 1:
            print(f"{var.name}: {var.varValue}")