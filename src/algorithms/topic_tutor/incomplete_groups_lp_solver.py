from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpBinary, PULP_CBC_CMD, GLPK_CMD, COIN_CMD
import pulp

class IncompleteGroupsLPSolver:
    def __init__(self, groups):
        self.groups = groups

    def filter_groups(self):
        """
        Filters the groups to keep only those with fewer than 4 students.
        """
        self.groups = [group for group in self.groups if len(group.students) < 4]

    def solve(self):
        """
        Solves the group assignment problem.

        1. Filters the incomplete groups.
        2. Defines decision variables for merging groups.
        3. Applies constraints to ensure each group participates in only one combination.
        4. Defines the objective function to maximize the number of complete groups formed.
        5. Executes the solver to find the optimal solution.
        """
        # Filter incomplete groups
        self.filter_groups()
        group_ids = [group.id for group in self.groups]

        # Define the optimization problem
        prob = LpProblem("Asignación de Grupos", LpMaximize)
        
        # Decision variables: if two groups merge
        x_vars_2 = LpVariable.dicts("Union", [tuple(sorted((i, j)))
                                              for i in group_ids
                                              for j in group_ids
                                              if i != j and len(self._get_group_by_id(i).students) + len(self._get_group_by_id(j).students) == 4], 0, 1, LpBinary)

        # Decision variables: if three groups merge
        x_vars_3 = LpVariable.dicts("Union", [tuple(sorted((i, j, k)))
                                              for i in group_ids
                                              for j in group_ids
                                              for k in group_ids
                                              if i != j and j != k and i != k and len(self._get_group_by_id(i).students) + len(self._get_group_by_id(j).students) + len(self._get_group_by_id(k).students) == 4], 0, 1, LpBinary)

        # Decision variables: if four groups merge
        x_vars_4 = LpVariable.dicts("Union", [tuple(sorted((i, j, k, l)))
                                              for i in group_ids
                                              for j in group_ids
                                              for k in group_ids
                                              for l in group_ids
                                              if i != j and j != k and i != k and i != l and j != l and k != l and len(self._get_group_by_id(i).students) + len(self._get_group_by_id(j).students) + len(self._get_group_by_id(k).students) + len(self._get_group_by_id(l).students) == 4], 0, 1, LpBinary)

        # Constraint: each group can merge only once
        for i in group_ids:
            related_vars_2 = [var for var in x_vars_2 if i in var]
            related_vars_3 = [var for var in x_vars_3 if i in var]
            related_vars_4 = [var for var in x_vars_4 if i in var]

            prob += lpSum(x_vars_2[var] for var in related_vars_2) + \
                    lpSum(x_vars_3[var] for var in related_vars_3) + \
                    lpSum(x_vars_4[var] for var in related_vars_4) <= 1

        # Objective function: maximize the number of complete groups formed and consider topic preferences
        obj = lpSum(x_vars_2) + lpSum(x_vars_3) + lpSum(x_vars_4)

        # Adjust the objective function according to topic matches
        for i in group_ids:
            for j in group_ids:
                if i < j:
                    match_count = sum(1 for topic in self._get_group_by_id(i).topics if topic.id in [t.id for t in self._get_group_by_id(j).topics])
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
        # Solve the optimization problem
        solver = PULP_CBC_CMD(timeLimit=180, msg=False)
        # solver = GLPK_CMD(timeLimit=180, msg=True)
        # solver = COIN_CMD(timeLimit=180, msg=True)
        prob.solve(solver)

        # Identify the groups that were not merged
        assigned_groups = set()
        for var in prob.variables():
            if var.varValue == 1:
                group_indices = [int(idx) for idx in var.name.replace("Union_", "").replace("(", "").replace(")", "").split(",_")]
                assigned_groups.update(group_indices)
        print(assigned_groups)
        self.remaining_groups = [group for group in self.groups if group.id not in assigned_groups]

        # Merge the remaining groups into as many teams as possible
        self._merge_remaining_groups()

        print("Variables de decisión con valor 1:")
        for var in prob.variables():
            if "Union" in var.name and var.varValue == 1:
                print(f"{var.name}: {var.varValue}")

        return prob

    def _merge_remaining_groups(self):
        """
        Merges the remaining groups into as many teams as possible,
        ensuring that each merged team has at most 4 students.
        """
        while len(self.remaining_groups) > 1:
            group = self.remaining_groups.pop(0)
            for other_group in self.remaining_groups:
                if len(group.students) + len(other_group.students) <= 4:
                    print(f"Unión adicional: Grupo {group.id} con Grupo {other_group.id}")
                    group.students.extend(other_group.students)
                    self.remaining_groups.remove(other_group)
                    break

    def _get_group_by_id(self, id):
        """
        Retrieves a group by its ID.

        :param id: The ID of the group.
        :return: The group corresponding to the ID, or None if not found.
        """
        for group in self.groups:
            if group.id == id:
                return group
        return None
