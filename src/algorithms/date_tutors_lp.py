import pyscipopt as scip
from typing import List, Tuple

from src.model.group.final_state_group import FinalStateGroup
from src.model.tutor.tutor import Tutor
from src.model.utils.date import Date
from src.model.utils.hour import Hour

class DateTutorsLPSolver:

    def __init__(self, dates: List[Date], groups: List[FinalStateGroup], tutors: List[Tutor]):
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
            mutual_available_dates = [
                (date.day, date.week, hour.name)
                for date in group.available_dates
                for hour in date.hours
                if date in tutor.available_dates and hour in tutor.available_dates[tutor.available_dates.index(date)].hours
            ]

            for day, week, hour in mutual_available_dates:
                var_name = f"assign_{group.id}_{tutor.id}_{day}_{week}_{hour}"
                self._decision_variables[(group.id, tutor.id, day, week, hour)] = self._model.addVar(
                    var_name, vtype="B", obj=0, lb=0, ub=1
                )
                if (tutor.id, day, week, hour) not in self._tutor_day_vars:
                    day_var_name = f"day_{tutor.id}_{day}_{week}_{hour}"
                    self._tutor_day_vars[(tutor.id, day, week, hour)] = self._model.addVar(
                        day_var_name, vtype="B", obj=0, lb=0, ub=1
                    )

    def groups_assignment_restriction(self):
        """Cada grupo se debe asignar una sola vez a una fecha y hora específica"""
        for date in self._available_dates:
            for hour in date.hours:
                self._model.addCons(
                    scip.quicksum(
                        self._decision_variables[(group.id, tutor.id, date.day, date.week, hour.name)]
                        for group in self._groups
                        for tutor in self._tutors
                        if (group.id, tutor.id, date.day, date.week, hour.name) in self._decision_variables
                    )
                    <= 1
                )
        """cada grupo se asigne exactamente una vez a una combinación de fecha y hora."""
        for group in self._groups:
            self._model.addCons(
                scip.quicksum(
                    self._decision_variables[(group.id, tutor.id, date.day, date.week, hour.name)]
                    for tutor in self._tutors
                    for date in group.available_dates
                    for hour in date.hours
                    if (group.id, tutor.id, date.day, date.week, hour.name) in self._decision_variables
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
                    if var[2] == date.day and var[3] == date.week
                )
                <= 5
            )

    def tutor_day_minimization_restriction(self):
        """Minimizar los días de asistencia de los tutores"""
        for tutor_id, day, week, hour in self._tutor_day_vars:
            self._model.addCons(
                self._tutor_day_vars[(tutor_id, day, week, hour)]
                >= scip.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[2] == day and var[3] == week and var[4] == hour and var[1] == tutor_id
                )
                / len(self._available_dates)
            )

    def define_objective(self):
        # Minimizar el número de días que asisten los tutores
        self._model.setObjective(
            scip.quicksum(
                week * self._tutor_day_vars[(tutor_id, day, week, hour)] # Chequear, multiplico por week para que se asigne primero y no en las ultimas semanas
                for (tutor_id, day, week, hour) in self._tutor_day_vars
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
                print(f"Variable {var} ((Grupo, Tutor, Dia, Semana, Hora): {var}")
                for group in self._groups:
                    if group.id == var[0]:
                        group.set_evaluation_date(Date(var[2], var[3], [Hour[var[4]]]))
                        result.append(group)

        print("\nVariables adicionales activadas (Tutor, Fecha, Hora):")
        for var in self._tutor_day_vars:
            if self._model.getVal(self._tutor_day_vars[var]) > 0:
                print(f"Variable adicional {var}")

        return result