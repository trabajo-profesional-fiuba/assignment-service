from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpBinary, PULP_CBC_CMD
import re

def create_assignment_variables(groups, professors, topics):
    assignment_vars = {}
    for i, group in enumerate(groups, 1):
        for topic in topics:
            for professor in professors:
                if topic[0] in professor[2]:
                    assignment_vars[(i, topic[0], professor[0])] = LpVariable(f"Asignación_{i}_{topic[0]}_{professor[0]}", 0, 1, LpBinary)
    return assignment_vars

def define_objective(prob, assignment_vars, groups, professors, topics):
    topic_scores = {(i, topic[0]): 0 for i in range(1, len(groups)+1) for topic in topics}
    for i, group in enumerate(groups, 1):
        for j, topic in enumerate(group[1]):
            topic_scores[(i, topic)] = len(group[1]) - j
    prob += lpSum(topic_scores[(i, topic[0])] * assignment_vars[(i, topic[0], professor[0])] for i in range(1, len(groups)+1) for topic in topics for professor in professors if topic[0] in professor[2])

def add_constraints(prob, assignment_vars, groups, professors, topics):
    for i, group in enumerate(groups, 1):
        prob += lpSum(assignment_vars[(i, topic, professor[0])] for topic in group[1] for professor in professors if topic in professor[2]) == 1

    for topic in topics:
        prob += lpSum(assignment_vars[(i, topic[0], professor[0])] for i in range(1, len(groups)+1) for professor in professors if topic[0] in professor[2]) <= topic[1]['capacity']

    for professor in professors:
        assigned_topics = [topic[0] for topic in topics if topic[0] in professor[2]]
        prob += lpSum(assignment_vars[(i, topic, professor[0])] for i in range(1, len(groups)+1) for topic in assigned_topics) <= professor[1]['capacity']

def solve(prob):
    prob.solve(PULP_CBC_CMD(msg=0))
    result_variables = []

    for var in prob.variables():
        if var.varValue == 1:
            result_variables.append(var.name)
    
    return result_variables

def simplex(groups, professors, topics):
    # Inicializar el problema de optimización
    prob = LpProblem("Asignación de Grupos", LpMaximize)

    # Crear variables de asignación
    assignment_vars = create_assignment_variables(groups, professors, topics)

    # Definir la función objetivo
    define_objective(prob, assignment_vars, groups, professors, topics, )

    # Agregar restricciones
    add_constraints(prob, assignment_vars, groups, professors, topics)

    # Resolver el problema de optimización
    result = solve(prob)

    teams_topics_professors = get_results(result)

    return teams_topics_professors

def get_results(result: {}):
    """Returns algorithm results."""
    original_dict = {}
    pattern = re.compile(r'Asignación_(\d+)_(\w+)_(\w+)')
    for var_name in result:
        match = pattern.match(var_name)
        if match:
            i, topic, professor = match.groups()
            i = int(i)
            if i not in original_dict:
                original_dict[i] = {}
            original_dict[i][topic] = professor

    return original_dict
