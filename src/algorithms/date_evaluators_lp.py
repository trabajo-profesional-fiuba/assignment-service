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
                    and group_date in evaluator.available_dates
                ):
                    var_name = f"assign_{group.id}_{group_date}_{evaluator.id}"
                    self._decision_variables[(group.id, group_date, evaluator.id)] = (
                        self._model.addVar(var_name, vtype="B", obj=0, lb=0, ub=1)
                    )

                    if (evaluator.id, group_date) not in self._evaluator_day_vars:
                        day_var_name = f"day_{evaluator.id}_{group_date}"
                        self._evaluator_day_vars[(evaluator.id, group_date)] = (
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
                if group.evaluation_date in evaluator.available_dates
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
        for evaluator_id, date in self._evaluator_day_vars:
            self._model.addCons(
                self._evaluator_day_vars[(evaluator_id, date)]
                >= scip.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[1] == date and var[2] == evaluator_id
                )
                / len(self._available_dates)
            )

    def evaluator_group_assignment_restriction(self):
        """Si un evaluador trabaja un día, se le asignan todos los grupos presentes ese
        día hasta un máximo de 5"""
        for evaluator in self._evaluators:
            for date in self._available_dates:
                if (evaluator.id, date) in self._evaluator_day_vars:
                    groups_on_date = [
                        group.id
                        for group in self._groups
                        if group.evaluation_date == date
                    ]
                    # Restricción de que un evaluador no evalúe más de 5 grupos por día
                    self._model.addCons(
                        scip.quicksum(
                            self._decision_variables[(group_id, date, evaluator.id)]
                            for group_id in groups_on_date
                            if (group_id, date, evaluator.id)
                            in self._decision_variables
                        )
                        <= 5,
                        name=f"max_5_groups_{evaluator.id}_{date}",
                    )

                    """ Restricción de que si un evaluador asiste en un día, evalúe
                    todos los grupos presentes ese día"""
                    for group_id in groups_on_date:
                        if (group_id, date, evaluator.id) in self._decision_variables:
                            self._model.addCons(
                                self._evaluator_day_vars[(evaluator.id, date)]
                                >= self._decision_variables[
                                    (group_id, date, evaluator.id)
                                ],
                                name=f"eval_assign_{evaluator.id}_{date}_{group_id}",
                            )

    def define_objective(self):
        # Minimizar el número de días que asisten los evaluadores
        self._model.setObjective(
            scip.quicksum(
                self._evaluator_day_vars[(evaluator_id, date)]
                for (evaluator_id, date) in self._evaluator_day_vars
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
                print(f"Variable {var} (Grupo, Fecha, Evaluador): {var}")
                result.append(var)

        print("\nVariables adicionales activadas (Evaluador, Fecha):")
        for var in self._evaluator_day_vars:
            if self._model.getVal(self._evaluator_day_vars[var]) > 0:
                print(f"Variable adicional {var}")

        return result
