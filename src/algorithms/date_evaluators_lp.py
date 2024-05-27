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
                mutual_available_dates = [
                    (date.day, date.week, hour)
                    for date in group.possible_evaluation_date
                    for hour in date.hours
                    if any(e_date.day == date.day and e_date.week == date.week and hour in e_date.hours for e_date in evaluator.available_dates)
                ]

                if (evaluator.id != group.tutor_id):
                    for day, week, hour in mutual_available_dates:
                        var_name = f"assign_{group.id}_{day.name}_{week}_{hour.name}_{evaluator.id}"
                        self._decision_variables[(group.id, day, week, hour, evaluator.id)] = self._model.addVar(
                            var_name, vtype="B", obj=0, lb=0, ub=1
                        )
                        if (evaluator.id, day, week) not in self._evaluator_day_vars:
                            day_var_name = f"day_{evaluator.id}_{day.name}_{week}"
                            self._evaluator_day_vars[(evaluator.id, day, week)] = self._model.addVar(
                                day_var_name, vtype="B", obj=0, lb=0, ub=1
                            )

    def groups_assignment_restriction(self):
        """Cada grupo se debe asignar entre 2 (si es posible) y 4 veces"""
        for group in self._groups:
            for date in group.possible_evaluation_date:
                for hour in date.hours:
                    available_evaluators = sum(
                        1
                        for evaluator in self._evaluators
                        for date_evaluator in evaluator._available_dates
                        if date.week == date_evaluator.week and date.day == date_evaluator.day and hour in evaluator.available_dates[evaluator.available_dates.index(date)].hours
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

            self._model.addCons(
                scip.quicksum(
                    self._decision_variables[(group.id, date.day, date.week, hour, evaluator.id)]
                    for date in group.possible_evaluation_date
                    for hour in date.hours
                    for evaluator in self._evaluators
                    if (group.id, date.day, date.week, hour, evaluator.id) in self._decision_variables
                )
                >= min_evaluators,
                name=f"unique_date_hour_{group.id}"
            )

    def evaluator_day_minimization_restriction(self):
        """Minimizar los días de trabajo de los evaluadores"""
        for evaluator_id, day, week in self._evaluator_day_vars:
            self._model.addCons(
                self._evaluator_day_vars[(evaluator_id, day, week)]
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
            # Restricción de que un evaluador no evalúe más de 5 grupos por semana
            weeks = set(date.week for date in self._available_dates)
            for week in weeks:
                self._model.addCons(
                    scip.quicksum(
                        self._decision_variables[var]
                        for var in self._decision_variables
                        if var[2] == week
                        and var[4] == evaluator.id
                    )
                    <= 5,
                    name=f"max_5_groups_week_{evaluator.id}_{week}",
                )

    def define_objective(self):
        # Minimizar el número de días que asisten los evaluadores
        self._model.setObjective(
            scip.quicksum(
                (day.value + week) * self._evaluator_day_vars[(evaluator_id, day, week)]
                for (evaluator_id, day, week) in self._evaluator_day_vars
            ),
            "minimize",
        )
    
    def solve(self):
        self._model.setRealParam('limits/time', 600)  # Limitar el tiempo de solución a 600 segundos (10 minutos)
        self._model.setIntParam('limits/solutions', 100)  # Limitar el número de soluciones
        self._model.setRealParam('limits/gap', 0.01)  # Establecer un gap óptimo de 1%
        self._model.setIntParam('presolving/maxrounds', 0)  # Desactivar la presolución
        self._model.setIntParam('branching/random/priority', 100)  # Usar una estrategia de ramificación aleatoria

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
