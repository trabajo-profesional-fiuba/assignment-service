from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpBinary, PULP_CBC_CMD

class IncompleteGroupsLPSolver:
    def __init__(self, groups):
        self.groups = groups

    def filter_groups(self):
        self.groups = [group for group in self.groups if len(group.students) < 4]

    def solve(self):
        self.filter_groups()
        group_ids = [group.id for group in self.groups]

        prob = LpProblem("Asignación de Grupos", LpMaximize)
        print(self.groups)
        # Variables de decisión: si dos grupos se unen
        x_vars_2 = LpVariable.dicts("Union", [tuple(sorted((i, j)))
                                              for i in group_ids
                                              for j in group_ids
                                              if i != j and len(self._get_group_by_id(i).students) + len(self._get_group_by_id(j).students) == 4], 0, 1, LpBinary)

        # Variables de decisión: si tres grupos se unen
        x_vars_3 = LpVariable.dicts("Union", [tuple(sorted((i, j, k)))
                                              for i in group_ids
                                              for j in group_ids
                                              for k in group_ids
                                              if i != j and j != k and i != k and len(self._get_group_by_id(i).students) + len(self._get_group_by_id(j).students) + len(self._get_group_by_id(k).students) == 4], 0, 1, LpBinary)

        # Variables de decisión: si cuatro grupos se unen
        x_vars_4 = LpVariable.dicts("Union", [tuple(sorted((i, j, k, l)))
                                              for i in group_ids
                                              for j in group_ids
                                              for k in group_ids
                                              for l in group_ids
                                              if i != j and j != k and i != k and i != l and j != l and k != l and len(self._get_group_by_id(i).students) + len(self._get_group_by_id(j).students) + len(self._get_group_by_id(k).students) + len(self._get_group_by_id(l).students) == 4], 0, 1, LpBinary)

        # Restricción: cada grupo se une solo una vez
        for i in group_ids:
            related_vars_2 = [var for var in x_vars_2 if i in var]
            related_vars_3 = [var for var in x_vars_3 if i in var]
            related_vars_4 = [var for var in x_vars_4 if i in var]

            prob += lpSum(x_vars_2[var] for var in related_vars_2) + \
                    lpSum(x_vars_3[var] for var in related_vars_3) + \
                    lpSum(x_vars_4[var] for var in related_vars_4) <= 1

        # Función objetivo: maximizar la cantidad de grupos formados y tener en cuenta las preferencias de temas
        obj = lpSum(x_vars_2) + lpSum(x_vars_3) + lpSum(x_vars_4)

        # Ajustar la función objetivo según las coincidencias de tópicos
        for i in group_ids:
            for j in group_ids:
                if i < j:
                    match_count = sum(1 for topic in self._get_group_by_id(i).topics if topic.id in [t.id for t in self._get_group_by_id(j).topics])
                    # category_match_count = sum(1 for topic in self._get_group_by_id(i).topics for category in topic.categories if category in [cat for t in self._get_group_by_id(j).topics for cat in t.categories])
                    category_match_count = sum(1 for topic in self._get_group_by_id(i).topics if topic.category in [t.category for t in self._get_group_by_id(j).topics])
                    if match_count > 0:
                        if (i, j) in x_vars_2:
                            obj += match_count * 10 * x_vars_2[(i, j)]
                        for k in group_ids:
                            if i != k and j != k:
                                if (i, j, k) in x_vars_3:
                                    obj += match_count * 10 * x_vars_3[(i, j, k)]
                        for k in group_ids:
                            for l in group_ids:
                                if i != k and j != k and i != l and j != l and k != l:
                                    if (i, j, k, l) in x_vars_4:
                                        obj += match_count * 10 * x_vars_4[(i, j, k, l)]
                    elif category_match_count > 0:
                        if (i, j) in x_vars_2:
                            obj += category_match_count * 5 * x_vars_2[(i, j)]
                        for k in group_ids:
                            if i != k and j != k:
                                if (i, j, k) in x_vars_3:
                                    obj += category_match_count * 5 * x_vars_3[(i, j, k)]
                        for k in group_ids:
                            for l in group_ids:
                                if i != k and j != k and i != l and j != l and k != l:
                                    if (i, j, k, l) in x_vars_4:
                                        obj += category_match_count * 5 * x_vars_4[(i, j, k, l)]

        prob += obj
        print(prob)
        # Resolver el problema de optimización
        prob.solve()

       # Identificar los grupos que no se unieron
        assigned_groups = set()
        for var in prob.variables():
            if var.varValue == 1:
                group_indices = [int(idx) for idx in var.name.replace("Union_", "").replace("(", "").replace(")", "").split(",_")]
                assigned_groups.update(group_indices)
        print(assigned_groups)
        self.remaining_groups = [group for group in self.groups if group.id not in assigned_groups]

        # Unir los grupos restantes en la mayor cantidad posible de equipos
        self._merge_remaining_groups()

        print("Variables de decisión con valor 1:")
        for var in prob.variables():
            if "Union" in var.name and var.varValue == 1:
                print(f"{var.name}: {var.varValue}")

        return prob

    def _merge_remaining_groups(self):
        print(self.remaining_groups)
        while len(self.remaining_groups) > 1:
            group = self.remaining_groups.pop(0)
            for other_group in self.remaining_groups:
                if len(group.students) + len(other_group.students) <= 4:
                    print(f"Unión adicional: Grupo {group.id} con Grupo {other_group.id}")
                    group.students.extend(other_group.students)
                    self.remaining_groups.remove(other_group)
                    break

    def _get_group_by_id(self, id):
        for group in self.groups:
            if group.id == id:
                return group
        return None
