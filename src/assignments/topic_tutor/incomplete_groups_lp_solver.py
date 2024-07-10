from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpBinary, PULP_CBC_CMD

class IncompleteGroupsLPSolver:
    def __init__(self, groups):
        self.groups = groups

    def filter_groups(self):
        self.groups = [group for group in self.groups if len(group.students) < 4]

    def solve(self):
        self.filter_groups()
        n = len(self.groups)  # Número total de grupos
        group_ids = [group.id for group in self.groups]

        prob = LpProblem("Asignación de Grupos", LpMaximize)

        # Variables de decisión: si dos grupos se unen
        x_vars_2 = LpVariable.dicts("Unión", [tuple(sorted((i, j)))
                                              for i in group_ids
                                              for j in group_ids
                                              if i != j and len(self._get_group_by_id(i).students) + len(self._get_group_by_id(j).students) == 4], 0, 1, LpBinary)

        # Variables de decisión: si tres grupos se unen
        x_vars_3 = LpVariable.dicts("Unión", [tuple(sorted((i, j, k)))
                                              for i in group_ids
                                              for j in group_ids
                                              for k in group_ids
                                              if i != j and j != k and i != k and len(self._get_group_by_id(i).students) + len(self._get_group_by_id(j).students) + len(self._get_group_by_id(k).students) == 4], 0, 1, LpBinary)

        # Variables de decisión: si cuatro grupos se unen
        x_vars_4 = LpVariable.dicts("Unión", [tuple(sorted((i, j, k, l)))
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

        # Ajustar la función objetivo según las preferencias de temas
        for i in group_ids:
            for j in group_ids:
                if i < j:
                    match_count = sum(1 for topic in self._get_group_by_id(i).topics if topic.id in [t.id for t in self._get_group_by_id(j).topics])
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

        prob += obj

        # Resolver el problema de optimización
        prob.solve()

        print("Variables de decisión con valor 1:")
        for var in prob.variables():
            if var.varValue == 1:
                print(f"{var.name}: {var.varValue}")

        return prob

    def _get_group_by_id(self, id):
        for group in self.groups:
            if group.id == id:
                return group
        return None