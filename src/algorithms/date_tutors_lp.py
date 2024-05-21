import pyscipopt as scip


class DateTutorsLPSolver:

    def __init__(self, dates: list, groups: list, tutors: list):
        self._groups = groups
        self._tutors = tutors
        self._available_dates = dates
        self._decision_variables = {}
        self._tutor_day_vars = {}
        self._model = scip.Model()
        self._model.setIntParam("display/verblevel", 0)

    def create_group_tutors_evaluator_decision_variables(self):
        for group in self._groups:
            tutor = group.find_tutor(self._tutors)
            mutual_available_dates = list(
                set(group.available_dates) & set(tutor.available_dates)
            )

            for d in mutual_available_dates:
                var_name = f"assign_{group.id}_{tutor.id}_{d}"
                self._decision_variables[(group.id, tutor.id, d)] = self._model.addVar(
                    var_name, vtype="B", obj=0, lb=0, ub=1
                )

                if (tutor.id, d) not in self._tutor_day_vars:
                    day_var_name = f"day_{tutor.id}_{d}"
                    self._tutor_day_vars[(tutor.id, d)] = self._model.addVar(
                        day_var_name, vtype="B", obj=0, lb=0, ub=1
                    )

    def groups_assignment_restriction(self):
        """Cada grupo se debe asignar una sola vez"""
        for group in self._groups:
            self._model.addCons(
                scip.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[0] == group.id
                )
                == 1
            )

    def dates_assignment_restriction(self):
        """En cada fecha puede haber máximo 5 grupos"""
        for date in self._available_dates:
            self._model.addCons(
                scip.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[2] == date
                )
                <= 5
            )

    def tutor_day_minimization_restriction(self):
        """Minimizar los días de asistencia de los tutores"""
        for tutor_id, date in self._tutor_day_vars:
            self._model.addCons(
                self._tutor_day_vars[(tutor_id, date)]
                >= scip.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[2] == date and var[1] == tutor_id
                )
                / len(self._available_dates)
            )

    def define_objective(self):
        # Minimizar el número de días que asisten los tutores
        self._model.setObjective(
            scip.quicksum(
                self._tutor_day_vars[(tutor_id, date)]
                for (tutor_id, date) in self._tutor_day_vars
            ),
            "minimize",
        )

    def solve(self):
        self.create_group_tutors_evaluator_decision_variables()
        self.groups_assignment_restriction()
        self.dates_assignment_restriction()
        self.tutor_day_minimization_restriction()
        self.define_objective()

        # Resolver el modelo
        self._model.optimize()

        print("Estado:", self._model.getStatus())
        print("Valor óptimo de la función objetivo:", self._model.getObjVal())

        result = []
        print("Variables de decisión activadas:")
        for var in self._decision_variables:
            if self._model.getVal(self._decision_variables[var]) > 0:
                print(f"Variable {var} ((Grupo, Tutor, Fecha): {var}")
                for group in self._groups:
                    if group.id == var[0]:
                        group.set_evaluation_date(var[2])
                        result.append(group)

        print("\nVariables adicionales activadas (Tutor, Fecha):")
        for var in self._tutor_day_vars:
            if self._model.getVal(self._tutor_day_vars[var]) > 0:
                print(f"Variable adicional {var}")

        return result
