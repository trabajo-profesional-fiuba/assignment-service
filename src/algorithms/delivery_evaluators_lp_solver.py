import pyscipopt as scip


class DateEvaluatorsLPSolver:

    def __init__(self, dates, result_tutors, groups, evaluators):
        self._result_tutors = result_tutors
        self._groups = groups
        self._evaluators = evaluators
        self._available_dates = dates
        self._decision_variables = {}
        self._evaluator_day_vars = {}
        self._model = scip.Model()
        self._model.setIntParam("display/verblevel", 0)

    def create_group_tutors_evaluator_decision_variables(self):
        for group in self._groups:
            for evaluator in self._evaluators:
                group_possible_dates = [
                    (g, t, week, day, hour)
                    for (g, t, week, day, hour) in self._result_tutors
                    if g == group.id
                ]
                print("Grupos 1:", group_possible_dates)
                mutual_available_dates = [
                    (week, day, hour)
                    for (g, t, week, day, hour) in group_possible_dates
                    for e_date in evaluator.available_dates
                    if day == e_date.day and week == e_date.week and hour == e_date.hour
                ]

                if evaluator.id != group.tutor.id:
                    for week, day, hour in mutual_available_dates:
                        var_name = (
                            f"assign_{group.id}_{week}_{day}_{hour}_{evaluator.id}"
                        )
                        self._decision_variables[
                            (group.id, week, day, hour, evaluator.id)
                        ] = self._model.addVar(var_name, vtype="B", obj=0, lb=0, ub=1)
                        if (evaluator.id, week, day) not in self._evaluator_day_vars:
                            day_var_name = f"day_{evaluator.id}_{week}_{day}"
                            self._evaluator_day_vars[(evaluator.id, week, day)] = (
                                self._model.addVar(
                                    day_var_name, vtype="B", obj=0, lb=0, ub=1
                                )
                            )

    def groups_assignment_restriction(self):
        for group in self._groups:
            group_date_vars = {}
            group_possible_dates = [
                (week, day, hour)
                for (g, t, week, day, hour) in self._result_tutors
                if g == group.id
            ]
            print("Grupos", group_possible_dates)
            for date in group_possible_dates:
                group_date_var = self._model.addVar(
                    f"group_date_{group.id}_{date[0]}_{date[1]}_{date[2]}",
                    vtype="B",
                    obj=0,
                    lb=0,
                    ub=1,
                )
                group_date_vars[date] = group_date_var
                self._model.addCons(
                    group_date_var
                    >= scip.quicksum(
                        self._decision_variables[
                            (group.id, date[0], date[1], date[2], evaluator.id)
                        ]
                        for evaluator in self._evaluators
                        if (group.id, date[0], date[1], date[2], evaluator.id)
                        in self._decision_variables
                    )
                    / len(self._evaluators),
                    name=f"group_date_{group.id}_{date[0]}_{date[1]}_{date[2]}",
                )
            self._model.addCons(
                scip.quicksum(group_date_vars.values()) == 1,
                name=f"unique_date_{group.id}",
            )
        for group in self._groups:
            group_possible_dates = [
                (week, day, hour)
                for (g, t, week, day, hour) in self._result_tutors
                if g == group.id
            ]
            print("Grupos 2:", group_possible_dates)

            for date in group_possible_dates:
                available_evaluators = sum(
                    1
                    for evaluator in self._evaluators
                    for date_evaluator in evaluator.available_dates
                    if date[0] == date_evaluator.week
                    and date[1] == date_evaluator.day
                    and date[2] == date_evaluator.hour
                )

            min_evaluators = min(2, available_evaluators)
            self._model.addCons(
                scip.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[0] == group.id
                )
                <= 4,
                name=f"max_assign_{group.id}",
            )

            self._model.addCons(
                scip.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[0] == group.id
                )
                >= min_evaluators,
                name=f"min_assign_{group.id}",
            )

    def evaluator_day_minimization_restriction(self):
        """Minimizar los días de trabajo de los evaluadores"""
        for evaluator_id, week, day in self._evaluator_day_vars:
            self._model.addCons(
                self._evaluator_day_vars[(evaluator_id, week, day)]
                >= scip.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[1] == week and var[2] == day and var[4] == evaluator_id
                )
                / len(self._available_dates)
            )

    def evaluator_group_assignment_restriction(self):
        """Si un evaluador trabaja un día, se le asignan todos los grupos presentes ese
        día hasta un máximo de 5. Además, un evaluador no debe
        evaluar más de 5 grupos por semana"""

        for evaluator in self._evaluators:
            # Restricción de que un evaluador no evalúe más de 5 grupos por semana
            weeks = set(date.week for date in self._available_dates)
            for week in weeks:
                self._model.addCons(
                    scip.quicksum(
                        self._decision_variables[var]
                        for var in self._decision_variables
                        if var[1] == week and var[4] == evaluator.id
                    )
                    <= 5,
                    name=f"max_5_groups_week_{evaluator.id}_{week}",
                )

    def define_objective(self):
        # Minimizar el número de días que asisten los evaluadores
        """"""
        self._model.setObjective(
            scip.quicksum(
                self._evaluator_day_vars[(evaluator_id, day, week)]
                for (evaluator_id, day, week) in self._evaluator_day_vars
            ),
            "minimize",
        )

    def solve(self):
        self.create_group_tutors_evaluator_decision_variables()
        self.groups_assignment_restriction()
        self.evaluator_day_minimization_restriction()
        self.evaluator_group_assignment_restriction()
        self.define_objective()

        self._model.optimize()

        print("Estado:", self._model.getStatus())
        print("Valor óptimo de la función objetivo:", self._model.getObjVal())

        result = []
        print("Variables de decisión activadas:")
        for var in self._decision_variables:
            if self._model.getVal(self._decision_variables[var]) > 0:
                print(f"Variable {var} (Grupo, Dia, Semana, Hora, Evaluador): {var}")
                result.append(var)

        print("\nVariables adicionales activadas (Evaluador, Dia, Semana, Hora):")
        for var in self._evaluator_day_vars:
            if self._model.getVal(self._evaluator_day_vars[var]) > 0:
                print(f"Variable adicional {var}")

        return result
