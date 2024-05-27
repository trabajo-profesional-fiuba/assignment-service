import pyscipopt as scip
from typing import List, Tuple

from src.model.group.final_state_group import FinalStateGroup
from src.model.tutor.tutor import Tutor
from src.model.utils.date import Date
from src.model.utils.hour import Hour

class DateTutorsLPSolver:

    def __init__(self, dates: List[Date], groups: List[FinalStateGroup], tutors: List[Tutor], num_weeks: int):
        self._groups = groups
        self._tutors = tutors
        self._available_dates = dates
        self._num_weeks = num_weeks
        self._decision_variables = {}
        self._tutor_day_vars = {}
        self._model = scip.Model()
        self._model.setIntParam("display/verblevel", 0)

    def create_group_tutors_evaluator_decision_variables(self, num_week: int):
        for group in self._groups:
            tutor = group.find_tutor(self._tutors)
            mutual_available_dates = [
                (date.day, date.week, hour)
                for date in self.dates_in_week(group.available_dates, num_week)
                for hour in date.hours
                if any(t_date.day == date.day and t_date.week == date.week and hour in t_date.hours for t_date in tutor.available_dates)
            ]

            for day, week, hour in mutual_available_dates:
                var_name = f"assign_{group.id}_{tutor.id}_{day.name}_{week}_{hour.name}"
                self._decision_variables[(group.id, tutor.id, day, week, hour)] = self._model.addVar(
                    var_name, vtype="B", obj=0, lb=0, ub=1
                )
                if (tutor.id, day, week, hour) not in self._tutor_day_vars:
                    day_var_name = f"day_{tutor.id}_{day.name}_{week}"
                    self._tutor_day_vars[(tutor.id, day, week)] = self._model.addVar(
                        day_var_name, vtype="B", obj=0, lb=0, ub=1
                    )

    def groups_assignment_restriction(self, num_week: int):
        """Cada grupo se debe asignar una sola vez a una fecha y hora específica"""
        for date in self.dates_in_week(self._available_dates, num_week):
            for hour in date.hours:
                self._model.addCons(
                    scip.quicksum(
                        self._decision_variables[(group.id, tutor.id, date.day, date.week, hour)]
                        for group in self._groups
                        for tutor in self._tutors
                        if (group.id, tutor.id, date.day, date.week, hour) in self._decision_variables
                    )
                    <= 1
                )
        """cada grupo se asigne exactamente una vez a una combinación de fecha y hora."""
        for group in self._groups:
            variables = [
                self._decision_variables[(group.id, tutor.id, date.day, date.week, hour)]
                for tutor in self._tutors
                for date in group.available_dates
                for hour in date.hours
                if (group.id, tutor.id, date.day, date.week, hour) in self._decision_variables
            ]
            if variables: 
                self._model.addCons(
                    scip.quicksum(variables)
                    == 1
                )

    def tutor_max_groups_per_date_restriction(self, num_week: int):
        """Each tutor can have at most 5 groups on a given date."""
        for tutor in self._tutors:
            for date in self.dates_in_week(self._available_dates, num_week):
                self._model.addCons(
                    scip.quicksum(
                        self._decision_variables[var]
                        for var in self._decision_variables
                        if var[2] == date.day and var[3] == date.week and var[1] == tutor.id
                    )
                    <= 5
                )
            
    def tutor_day_minimization_restriction(self, num_week: int):
        """Minimizar los días de asistencia de los tutores"""
        for tutor_id, day, week in self._tutor_day_vars:
            self._model.addCons(
                self._tutor_day_vars[(tutor_id, day, week)]
                >= scip.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[2] == day and var[3] == week and var[1] == tutor_id
                )
                / len(self.dates_in_week(self._available_dates, num_week))
            )

    def define_objective(self):
        # Minimizar el número de días que asisten los tutores
        self._model.setObjective(
            scip.quicksum(
                day.value * self._tutor_day_vars[(tutor_id, day, week)] # Chequear, multiplico por week y day para que se asigne primero y no en las ultimas semanas
                for (tutor_id, day, week) in self._tutor_day_vars
            ),
            "minimize",
        )

    def dates_in_week(self, dates: list, num_week: int):
        dates_week = []
        for date in dates:
            if date.week == num_week:
                dates_week.append(date)
        return dates_week
    
    def solve(self):
        all_results = []

        for num_week in range(1, self._num_weeks + 1):

            # Reinicia el modelo y las variables para cada semana
            self._model.freeTransform()
            self._model = scip.Model()
            self._model.setIntParam("display/verblevel", 0)
            self._decision_variables = {}
            self._tutor_day_vars = {}

            # Crea las variables de decisión y restricciones solo para la semana actual
            self.create_group_tutors_evaluator_decision_variables(num_week)
            self.groups_assignment_restriction(num_week)
            self.tutor_max_groups_per_date_restriction(num_week)
            self.tutor_day_minimization_restriction(num_week)
            self.define_objective()

            # Resolver el modelo para la semana actual
            self._model.optimize()

            print(f"Estado para la semana {num_week}:", self._model.getStatus())
            print(f"Valor óptimo de la función objetivo para la semana {num_week}:", self._model.getObjVal())

            week_result = []
            print(f"Variables de decisión activadas para la semana {num_week}:")
            for var in self._decision_variables:
                if self._model.getVal(self._decision_variables[var]) > 0:
                    print(f"Variable {var} ((Grupo, Tutor, Dia, Semana, Hora): {var}")
                    for group in self._groups:
                        if group.id == var[0]:
                            group.set_possible_evaluation_date(Date(var[2], var[3], [var[4]]))
                            week_result.append(group)
                            all_results.append(group)

            print(f"\nVariables adicionales activadas para la semana {num_week} (Tutor, Fecha, Hora):")
            for var in self._tutor_day_vars:
                if self._model.getVal(self._tutor_day_vars[var]) > 0:
                    print(f"Variable adicional {var}")

        return all_results