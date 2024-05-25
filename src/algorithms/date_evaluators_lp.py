import pyscipopt as scip


class DateEvaluatorsLPSolver:

    def __init__(self, dates: list, groups: list, evaluators: list):
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
                group_date = group.evaluation_date
                if (
                    evaluator.id != group.tutor_id
                    and self.is_date_in_available_dates(group_date, evaluator.available_dates)
                ):
                    var_name = f"assign_{group.id}_{group_date.day}_{group_date.week}_{group_date.hours[0].name}_{evaluator.id}"
                    self._decision_variables[(group.id, group_date.day, group_date.week, group_date.hours[0].name, evaluator.id)] = (
                        self._model.addVar(var_name, vtype="B", obj=0, lb=0, ub=1)
                    )

                    if (evaluator.id, group_date.day, group_date.week, group_date.hours[0].name) not in self._evaluator_day_vars:
                        day_var_name = f"day_{evaluator.id}_{group_date.day}_{group_date.week}_{group_date.hours[0].name}"
                        self._evaluator_day_vars[(evaluator.id, group_date.day, group_date.week, group_date.hours[0].name)] = (
                            self._model.addVar(
                                day_var_name, vtype="B", obj=0, lb=0, ub=1
                            )
                        )

    def groups_assignment_restriction(self):
        """Cada grupo se debe asignar entre 2 (si es posible) y 4 veces"""
        for group in self._groups:
            available_evaluators = sum(
                1
                for evaluator in self._evaluators
                if self.is_date_in_available_dates(group.evaluation_date, evaluator.available_dates)
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
        for evaluator_id, day, week, hour in self._evaluator_day_vars:
            self._model.addCons(
                self._evaluator_day_vars[(evaluator_id, day, week, hour)]
                >= scip.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[1] == day and var[2] == week and var[4] == evaluator_id
                )
                / len(self._available_dates) 
            )

    def evaluator_group_assignment_restriction(self):
        """Si un evaluador trabaja un día, se le asignan todos los grupos presentes ese
        día hasta un máximo de 5. Además, un evaluador no debe evaluar más de 5 grupos por semana"""

        for evaluator in self._evaluators:
            # for date in self._available_dates:
                # if (evaluator.id, date.day, date.week) in self._evaluator_day_vars:
                #     groups_on_date_day = [
                #         group.id
                #         for group in self._groups
                #         if group.evaluation_date.day == date.day and group.evaluation_date.week == date.week
                #     ]

                # # Restricción de que un evaluador no evalúe más de 5 grupos por día
                # self._model.addCons(
                #     scip.quicksum(
                #         self._decision_variables[(group_id, date.day, date.week, hour.name, evaluator.id)]
                #         for group_id in groups_on_date_day
                #         for hours in evaluator.available_dates
                #         for hour in hours
                #         if (group_id, date.day, date.week, hour.name, evaluator.id) in self._decision_variables
                #     )
                #     <= 5,
                #     name=f"max_5_groups_day_{evaluator.id}_{date.day}_{date.week}",
                # )

            # Restricción de que un evaluador no evalúe más de 5 grupos por semana
            weeks = set(date.week for date in self._available_dates)
            for week in weeks:
                self._model.addCons(
                    scip.quicksum(
                        self._decision_variables[(group.id, date.day, date.week, hour.name, evaluator.id)]
                        for group in self._groups
                        for date in evaluator.available_dates
                        for hour in date.hours
                        if date.week == week
                        and (group.id, date.day, date.week, hour.name, evaluator.id) in self._decision_variables
                    )
                    <= 5,
                    name=f"max_5_groups_week_{evaluator.id}_{week}",
                )

                # if (evaluator.id, date) in self._evaluator_day_vars:
                #     groups_on_date = [
                #         group.id
                #         for group in self._groups
                #         if group.evaluation_date == date
                #     ]
                #     # Restricción de que un evaluador no evalúe más de 5 grupos por día
                #     self._model.addCons(
                #         scip.quicksum(
                #             self._decision_variables[(group_id, date, evaluator.id)]
                #             for group_id in groups_on_date
                #             if (group_id, date, evaluator.id)
                #             in self._decision_variables
                #         )
                #         <= 5,
                #         name=f"max_5_groups_{evaluator.id}_{date}",
                #     )

                #     """ Restricción de que si un evaluador asiste en un día, evalúe
                #     todos los grupos presentes ese día"""
                #     for group_id in groups_on_date:
                #         if (group_id, date, evaluator.id) in self._decision_variables:
                #             self._model.addCons(
                #                 self._evaluator_day_vars[(evaluator.id, date)]
                #                 >= self._decision_variables[
                #                     (group_id, date, evaluator.id)
                #                 ],
                #                 name=f"eval_assign_{evaluator.id}_{date}_{group_id}",
                #             )

    def define_objective(self):
        # Minimizar el número de días que asisten los evaluadores
        self._model.setObjective(
            scip.quicksum(
                self._evaluator_day_vars[(evaluator_id, day, week, hour)]
                for (evaluator_id, day, week, hour) in self._evaluator_day_vars
            ),
            "minimize",
        )

    def is_date_in_available_dates(self, group_date, available_dates):
        for date in available_dates:
            if (
                date.day == group_date.day and
                date.week == group_date.week and
                any(hour in date.hours for hour in group_date.hours)
            ):
                return True
        return False
    
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
