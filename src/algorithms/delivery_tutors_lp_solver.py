import pyscipopt as scip
from src.constants import DATE_ID, GROUP_ID, TUTOR_ID


class DeliveryTutorsLPSolver:
    """
    Class to solve the problem of assigning dates to groups using linear programming.

    Attributes:
    -----------
    _groups : list
        List of groups with their tutors.
    _tutors : list
        List of available tutors.
    _available_dates : list
        List of available dates.
    _decision_variables : dict
        Decision variables for the assignment.
    _tutor_day_vars : dict
        Variables to minimize the attendance days of tutors.
    _model : scip.Model
        SCIP model to solve the problem.
    """

    def __init__(self, dates, groups, tutors):
        """
        Initializes the class with dates, groups, and tutors.

        Parameters:
        -----------
        dates : list
            List of available dates.
        groups : list
            List of groups that need tutors.
        tutors : list
            List of available tutors.
        """
        self._groups = groups
        self._tutors = tutors
        self._available_dates = dates
        self._decision_variables = {}
        self._tutor_day_vars = {}
        self._model = scip.Model()
        self._model.setIntParam("display/verblevel", 0)

    def create_group_tutors_evaluator_decision_variables(self, num_week: int):
        """
        Creates decision variables for the assignment of dates to groups.
        Decision variables: group-id-tutor-id-date-week-day-hour
        Tutor variables: tutor-id-date-week-day

        Parameters:
        -----------
        num_week : int
            The week number for which the variables are being created.
        """
        for group in self._groups:
            tutor = group.tutor
            mutual_available_dates = [
                (date.week, date.day, date.hour)
                for date in self.dates_in_week(group.state.available_dates, num_week)
                if any(
                    t_date.week == date.week
                    and t_date.day == date.day
                    and date.hour == t_date.hour
                    for t_date in tutor.state.available_dates
                )
            ]

            for week, day, hour in mutual_available_dates:
                var_name = f"{GROUP_ID}-{group.id}-{TUTOR_ID}-{tutor.id}-{DATE_ID}\
                -{week}-{day}-{hour}"
                self._decision_variables[(group.id, tutor.id, week, day, hour)] = (
                    self._model.addVar(var_name, vtype="B", obj=0, lb=0, ub=1)
                )
                if (tutor.id, week, day, hour) not in self._tutor_day_vars:
                    day_var_name = f"{TUTOR_ID}-{tutor.id}-{DATE_ID}-{week}-{day}"
                    self._tutor_day_vars[(tutor.id, week, day)] = self._model.addVar(
                        day_var_name, vtype="B", obj=0, lb=0, ub=1
                    )

    def groups_assignment_restriction(self, num_week: int):
        """
        Adds group assignment restrictions to the model.

        Parameters:
        -----------
        num_week : int
            The week number for which the restrictions are being added.
        """
        # Cada grupo se debe asignar una sola vez a una fecha y hora específica
        for date in self.dates_in_week(self._available_dates, num_week):
            self._model.addCons(
                scip.quicksum(
                    self._decision_variables[
                        (group.id, tutor.id, date.week, date.day, date.hour)
                    ]
                    for group in self._groups
                    for tutor in self._tutors
                    if (group.id, tutor.id, date.week, date.day, date.hour)
                    in self._decision_variables
                )
                <= 1
            )
        # Cada grupo se asigne exactamente una vez a una
        # combinación de fecha y hora.
        for group in self._groups:
            variables = [
                self._decision_variables[
                    (group.id, tutor.id, date.week, date.day, date.hour)
                ]
                for tutor in self._tutors
                for date in group.state.available_dates
                if (group.id, tutor.id, date.week, date.day, date.hour)
                in self._decision_variables
            ]
            if variables:
                self._model.addCons(scip.quicksum(variables) == 1)

    def tutor_max_groups_per_date_restriction(self, num_week: int):
        """
        Adds the restriction that each tutor can have at most 5 groups per day.

        Parameters:
        -----------
        num_week : int
            The week number for which the restrictions are being added.
        """
        for tutor in self._tutors:
            for date in self.dates_in_week(self._available_dates, num_week):
                self._model.addCons(
                    scip.quicksum(
                        self._decision_variables[var]
                        for var in self._decision_variables
                        if var[2] == date.week
                        and var[3] == date.day
                        and var[1] == tutor.id
                    )
                    <= 5
                )

    def tutor_day_minimization_restriction(self, num_week: int):
        """
        Minimizes the attendance days of tutors.

        Parameters:
        -----------
        num_week : int
            The week number for which the restrictions are being added.
        """
        for tutor_id, week, day in self._tutor_day_vars:
            self._model.addCons(
                self._tutor_day_vars[(tutor_id, week, day)]
                >= scip.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[2] == week and var[3] == day and var[1] == tutor_id
                )
                / len(self.dates_in_week(self._available_dates, num_week))
            )

    def define_objective(self):
        """
        Defines the objective of minimizing the number of days tutors attend.
        """
        self._model.setObjective(
            scip.quicksum(
                self._tutor_day_vars[(tutor_id, week, day)]
                for (tutor_id, week, day) in self._tutor_day_vars
            ),
            "minimize",
        )

    def dates_in_week(self, dates: list, num_week: int):
        """
        Filters dates to include only those in a specific week.

        Parameters:
        -----------
        dates : list
            List of dates.
        num_week : int
            Week number to filter.

        Returns:
        --------
        list
            List of dates filtered by week.
        """
        return [date for date in dates if date.week == num_week]

    def solve(self):
        """
        Solves the linear programming model for each week.

        Returns:
        --------
        list
            List of activated decision variables.
        """
        num_week = 1
        result = []

        while num_week <= max(date.week for date in self._available_dates):

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
            print(
                f"Valor óptimo de la función objetivo para la semana {num_week}:",
                self._model.getObjVal(),
            )

            print(f"Variables de decisión activadas para la semana {num_week}:")
            for var in self._decision_variables:
                if self._model.getVal(self._decision_variables[var]) > 0:
                    print(f"Variable {var} ((Grupo, Tutor, Semana, Día, Hora): {var}")
                    for group in self._groups:
                        if group.id == var[0]:
                            result.append(var)

            print(
                f"\nVariables activadas para la semana {num_week} (Tutor, Fecha, Hora):"
            )
            for var in self._tutor_day_vars:
                if self._model.getVal(self._tutor_day_vars[var]) > 0:
                    print(f"Variable adicional {var}")

            num_week += 1

        return result