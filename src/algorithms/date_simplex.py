import gurobipy as gp


class DateSimplexSolver:

    def __init__(self, dates: list, groups: list, tutors: list, evaluators: list):
        self._groups = groups
        self._tutors = tutors
        self._evaluators = evaluators
        self._avaliable_dates = dates
        self._decision_variables = {}
        self._evaluator_day_vars = {}
        self._tutor_day_vars = {}
        self._model = gp.Model("Group_Assignment")

    def create_group_tutors_evaluator_decision_variables(self):
        for group in self._groups:
            tutor = group.find_tutor(self._tutors)
            mutual_avaliable_dates = list(
                set(group.avaliable_dates) & set(tutor.avaliable_dates)
            )

            for evaluator in self._evaluators:
                if evaluator.id != tutor.id:
                    total_avaliable_dates = list(
                        set(mutual_avaliable_dates) & set(evaluator.avaliable_dates)
                    )

                    for d in total_avaliable_dates:
                        var_name = f"assign_{group._id}_{tutor._id}_{d}_{evaluator._id}"
                        self._decision_variables[
                            (group._id, tutor._id, d, evaluator._id)
                        ] = self._model.addVar(vtype=gp.GRB.BINARY, name=var_name)

                        if (evaluator._id, d) not in self._evaluator_day_vars:
                            day_var_name = f"day_{evaluator._id}_{d}"
                            self._evaluator_day_vars[(evaluator._id, d)] = (
                                self._model.addVar(
                                    vtype=gp.GRB.BINARY, name=day_var_name
                                )
                            )

                        if (tutor._id, d) not in self._tutor_day_vars:
                            day_var_name = f"day_{tutor._id}_{d}"
                            self._tutor_day_vars[(tutor._id, d)] = self._model.addVar(
                                vtype=gp.GRB.BINARY, name=day_var_name
                            )

    def groups_assignment_restriction(self):
        """Cada grupo se debe asignar una sola vez"""
        for group in self._groups:
            self._model.addConstr(
                gp.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[0] == group._id
                )
                == 1
            )

    def dates_assignment_restriction(self):
        """En cada fecha puede haber máximo 5 grupos"""
        for date in self._avaliable_dates:
            self._model.addConstr(
                gp.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[2] == date
                )
                <= 5
            )

    def evaluator_day_minimization_restriction(self):
        """Minimizar los días de trabajo de los evaluadores"""
        for evaluator_id, date in self._evaluator_day_vars:
            self._model.addConstr(
                self._evaluator_day_vars[(evaluator_id, date)]
                >= gp.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[2] == date and var[3] == evaluator_id
                )
                / len(self._avaliable_dates)
            )

    def tutor_day_minimization_restriction(self):
        """Minimizar los días de asistencia de los tutores"""
        """Para cada tutor y fecha, se asegura que la variable correspondiente al 
        tutor y la fecha sea mayor o igual a la fracción de grupos asignados en esa fecha 
        para ese tutor en relación con el total de fechas disponibles"""
        
        for tutor_id, date in self._tutor_day_vars:
            self._model.addConstr(
                self._tutor_day_vars[(tutor_id, date)]
                >= gp.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[2] == date and var[1] == tutor_id
                )
                / len(self._avaliable_dates)
            )

    def define_objective(self):
        # Minimizar el número de días que trabajan tanto evaluadores como tutores
        self._model.setObjective(
            gp.quicksum(
                self._evaluator_day_vars[(evaluator_id, date)]
                for (evaluator_id, date) in self._evaluator_day_vars
            )
            + gp.quicksum(
                self._tutor_day_vars[(tutor_id, date)]
                for (tutor_id, date) in self._tutor_day_vars
            ),
            gp.GRB.MINIMIZE,
        )

    def solve(self):
        self.create_group_tutors_evaluator_decision_variables()
        self.groups_assignment_restriction()
        self.dates_assignment_restriction()
        self.evaluator_day_minimization_restriction()
        self.tutor_day_minimization_restriction()
        self.define_objective()

        # Desactivar los mensajes de salida de Gurobi
        self._model.setParam("OutputFlag", 0)  # 0 para simplex

        # Resolver el modelo
        self._model.optimize()

        print("Estado:", self._model.status)
        print("Éxito:", self._model.status == gp.GRB.OPTIMAL)
        print("Valor óptimo de la función objetivo:", self._model.objVal)

        result = []
        # Identificar las variables de decisión que finalizaron con valor distinto de cero
        for var in self._decision_variables:
            if self._decision_variables[var].x > 0:
                print(
                    f"Variable de decisión {var} (Grupo, Tutor, Fecha, Evaluador): {var}"
                )
                result.append(var)

        for var in self._evaluator_day_vars:
            if self._evaluator_day_vars[var].x > 0:
                print(f"Variable adicional (Evaluador, Fecha): {var}")

        for var in self._tutor_day_vars:
            if self._tutor_day_vars[var].x > 0:
                print(f"Variable adicional (Tutor, Fecha): {var}")

        return result
