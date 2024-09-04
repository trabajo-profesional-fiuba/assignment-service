import re
from pulp import (
    LpProblem,
    LpVariable,
    lpSum,
    LpMaximize,
    LpBinary,
    PULP_CBC_CMD,
)


from src.core.group_answer import GroupFormAnswer
from src.core.group_topic_preferences import GroupTopicPreferences


class IncompleteGroupsLPSolver:
    def __init__(self, groups):
        self.groups = groups
        self.formed_groups = []
        self.filtered_groups = self._filter_groups_with_4_students()
        self.remaining_groups = []

    def _filter_groups_with_4_students(self):
        """
        Filters the groups to keep only those with exactly 4 students.
        """
        return [group for group in self.groups if len(group.students) == 4]

    def filter_groups(self):
        """
        Filters the groups to keep only those with fewer than 4 students.
        """
        return [group for group in self.groups if len(group.students) < 4]

    def solve(self):
        # Filter incomplete groups
        filtered_groups = self.filter_groups()
        group_ids = [group.id for group in filtered_groups]

        # Define the optimization problem
        prob = LpProblem("Asignación de Grupos", LpMaximize)

        # Decision variables: if two groups merge
        x_vars_2 = LpVariable.dicts(
            "Union",
            [
                tuple(sorted((i, j)))
                for i in group_ids
                for j in group_ids
                if i != j
                and len(self._get_group_by_id(i).students)
                + len(self._get_group_by_id(j).students)
                == 4
            ],
            0,
            1,
            LpBinary,
        )

        # Decision variables: if three groups merge
        x_vars_3 = LpVariable.dicts(
            "Union",
            [
                tuple(sorted((i, j, k)))
                for i in group_ids
                for j in group_ids
                for k in group_ids
                if i != j
                and j != k
                and i != k
                and len(self._get_group_by_id(i).students)
                + len(self._get_group_by_id(j).students)
                + len(self._get_group_by_id(k).students)
                == 4
            ],
            0,
            1,
            LpBinary,
        )

        # Decision variables: if four groups merge
        x_vars_4 = LpVariable.dicts(
            "Union",
            [
                tuple(sorted((i, j, k, l)))
                for i in group_ids
                for j in group_ids
                for k in group_ids
                for l in group_ids
                if i != j
                and j != k
                and i != k
                and i != l
                and j != l
                and k != l
                and len(self._get_group_by_id(i).students)
                + len(self._get_group_by_id(j).students)
                + len(self._get_group_by_id(k).students)
                + len(self._get_group_by_id(l).students)
                == 4
            ],
            0,
            1,
            LpBinary,
        )

        # Constraint: each group can merge only once
        for i in group_ids:
            related_vars_2 = [var for var in x_vars_2 if i in var]
            related_vars_3 = [var for var in x_vars_3 if i in var]
            related_vars_4 = [var for var in x_vars_4 if i in var]

            prob += (
                lpSum(x_vars_2[var] for var in related_vars_2)
                + lpSum(x_vars_3[var] for var in related_vars_3)
                + lpSum(x_vars_4[var] for var in related_vars_4)
                <= 1
            )

        # Objective function: maximize the number of complete groups formed
        # and consider topic preferences
        obj = lpSum(x_vars_2) + lpSum(x_vars_3) + lpSum(x_vars_4)

        # Adjust the objective function according to topic matches
        for i in group_ids:
            for j in group_ids:
                if i < j:
                    match_count = sum(
                        1
                        for topic in self._get_group_by_id(i).topics
                        if topic.id in [t.id for t in self._get_group_by_id(j).topics]
                    )
                    category_match_count = sum(
                        1
                        for topic in self._get_group_by_id(i).topics
                        if topic.category
                        in [t.category for t in self._get_group_by_id(j).topics]
                    )
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
                                    obj += (
                                        category_match_count * 5 * x_vars_3[(i, j, k)]
                                    )
                        for k in group_ids:
                            for l in group_ids:
                                if i != k and j != k and i != l and j != l and k != l:
                                    if (i, j, k, l) in x_vars_4:
                                        obj += (
                                            category_match_count
                                            * 5
                                            * x_vars_4[(i, j, k, l)]
                                        )

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
                group_indices = re.findall(r"'([\d\.]+)'", var.name)
                assigned_groups.update(group_indices)
                self.formed_groups.append(
                    self._create_group_topic_preferences(group_indices)
                )

        self.remaining_groups = [
            group for group in filtered_groups if group.id not in assigned_groups
        ]

        # Merge the remaining groups into as many teams as possible
        self._merge_remaining_groups()

        print("Variables de decisión con valor 1:")
        for var in prob.variables():
            if "Union" in var.name and var.varValue == 1:
                print(f"{var.name}: {var.varValue}")

        return self.formed_groups + self.filtered_groups

    def _create_group_topic_preferences(self, group_indices):
        """
        Creates a new GroupTopicPreferences object by combining students and topics
        from the given group indices.

        :param group_indices: List of group IDs to merge.
        :return: A new GroupTopicPreferences object.
        """
        combined_students = []

        # Retrieve all groups involved
        groups = [self._get_group_by_id(group_id) for group_id in group_indices]

        # Find the group with the most students
        group_with_most_students = max(groups, key=lambda g: len(g.students))

        # Get topics that are common across all groups
        common_topics = set(group_with_most_students.topics)
        for group in groups:
            common_topics.intersection_update(set(group.topics))

        # Order common topics based on the group with most students
        common_topics_ordered = [
            topic for topic in group_with_most_students.topics if topic in common_topics
        ]

        # If common topics are less than 3, add more topics from the group with most\
        # students
        while len(common_topics_ordered) < 3:
            for topic in group_with_most_students.topics:
                if topic not in common_topics_ordered:
                    common_topics_ordered.append(topic)
                if len(common_topics_ordered) == 3:
                    break

        # Combine students from all groups
        for group in groups:
            combined_students.extend(group.students)

        new_group_id = group_with_most_students.id
        new_group = GroupFormAnswer(id=new_group_id)
        new_group.add_students(combined_students)
        new_group.add_topics(common_topics_ordered)
        return new_group

    def _merge_remaining_groups(self):
        """
        Merges the remaining groups into as many teams as possible,
        ensuring that each merged team has at most 4 students.
        """
        while len(self.remaining_groups) > 1:
            group = self.remaining_groups.pop(0)
            for other_group in self.remaining_groups:
                if len(group.students) + len(other_group.students) <= 4:
                    print(
                        f"Unión adicional: Grupo {group.id} con Grupo {other_group.id}"
                    )

                    # Crear un nuevo GroupTopicPreferences para el grupo unido
                    if len(group.students) > len(other_group.students):
                        new_group_id = group.id
                    else:
                        new_group_id = other_group.id

                    new_topics = self.combine_topics(group, other_group)
                    new_students = group.students + other_group.students

                    new_group = GroupFormAnswer(id=new_group_id)
                    new_group.add_students(new_students)
                    new_group.add_topics(new_topics)
                    # Añadir el nuevo grupo a formed_groups
                    self.formed_groups.append(new_group)

                    # Eliminar el grupo unido de remaining_groups
                    self.remaining_groups.remove(other_group)
                    break

        if len(self.remaining_groups) == 1:
            group = self.remaining_groups.pop(0)
            new_group = GroupFormAnswer(id=group.id)
            new_group.add_students(group.students)
            new_group.add_topics(group.topics)
            self.formed_groups.append(new_group)

    def combine_topics(self, group1, group2):
        """
        Combina los tópicos de dos grupos, manteniendo el orden y asegurando al
        menos 3 tópicos.
        """
        common_topics = set(group1.topics).intersection(set(group2.topics))
        all_topics = sorted(common_topics, key=lambda topic: group1.topics.index(topic))

        if len(all_topics) < 3:
            all_topics.extend(
                [t for t in group1.topics if t not in all_topics][: 3 - len(all_topics)]
            )

        return all_topics

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
