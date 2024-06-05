import pyscipopt as scip
from src.constants import DATE_ID, EVALUATOR_ID, GROUP_ID
from src.model.utils.delivery_date import DeliveryDate


class DateEvaluatorsLPSolver:
    """
    Class to solve the problem of assigning evaluators to groups
    using linear programming.

    Attributes:
    -----------
    _result_tutors : list
        List of results related to tutors.
    _groups : list
        List of groups that need evaluators.
    _evaluators : list
        List of available evaluators.
    _available_dates : list
        List of available dates.
    _decision_variables : dict
        Decision variables for the assignment.
    _evaluator_day_vars : dict
        Variables to minimize the attendance days of evaluators.
    _model : scip.Model
        SCIP model to solve the problem.
    """

    def __init__(self, dates, result_tutors, groups, evaluators):
        """
        Initializes the class with dates, result_tutors, groups, and evaluators.

        Parameters:
        -----------
        dates : list
            List of available dates.
        result_tutors : list
            List of results related to tutors.
        groups : list
            List of groups that need evaluators.
        evaluators : list
            List of available evaluators.
        """
        self._result_tutors = result_tutors
        self._groups = groups
        self._evaluators = evaluators
        self._available_dates = dates
        self._decision_variables = {}
        self._evaluator_day_vars = {}
        self._model = scip.Model()
        self._model.setIntParam("display/verblevel", 0)

    def create_decision_variables(self):
        """
        Creates decision variables for the assignment of evaluators to groups.
        """
        for group in self._groups:
            for evaluator in self._evaluators:
                self._create_variables_for_group_evaluator(group, evaluator)

    def _create_variables_for_group_evaluator(self, group, evaluator):
        """
        Creates decision variables for a specific group and evaluator.
        Decision variables: group-id-evaluator-id-date-week-day-hour
        Evaluator variables: evaluator-id-date-week-day

        Parameters:
        -----------
        group : Group
            A group that needs an evaluator.
        evaluator : Evaluator
            An evaluator available for assignment.
        """
        group_possible_dates = [
            (g, t, week, day, hour)
            for (g, t, week, day, hour) in self._result_tutors
            if g == group.id
        ]
        mutual_available_dates = [
            (week, day, hour)
            for (g, t, week, day, hour) in group_possible_dates
            for e_date in evaluator.available_dates
            if day == e_date.day and week == e_date.week and hour == e_date.hour
        ]

        if evaluator.id != group.tutor.id:
            for week, day, hour in mutual_available_dates:
                var_name = f"{GROUP_ID}-{group.id}-{EVALUATOR_ID}-{evaluator.id}-\
                {DATE_ID}-{week}-{day}-{hour}"
                self._decision_variables[(group.id, evaluator.id, week, day, hour)] = (
                    self._model.addVar(var_name, vtype="B", obj=0, lb=0, ub=1)
                )
                if (evaluator.id, week, day) not in self._evaluator_day_vars:
                    day_var_name = (
                        f"{EVALUATOR_ID}-{evaluator.id}-{DATE_ID}-{week}-{day}"
                    )
                    self._evaluator_day_vars[(evaluator.id, week, day)] = (
                        self._model.addVar(day_var_name, vtype="B", obj=0, lb=0, ub=1)
                    )

    def add_group_assignment_constraints(self):
        """
        Adds group assignment constraints to the model.
        """
        for group in self._groups:
            self._add_unique_date_constraint(group)
            self._add_min_max_assignment_constraints(group)

    def _add_unique_date_constraint(self, group):
        """
        Adds a constraint to ensure each group is assigned to a unique date.
        Group unique date variables: group-id-date-week-day-hour

        Parameters:
        -----------
        group : Group
            A group that needs an evaluator.
        """
        group_date_vars = {}
        group_possible_dates = [
            (week, day, hour)
            for (g, t, week, day, hour) in self._result_tutors
            if g == group.id
        ]
        if len(group_possible_dates) > 0:
            for date in group_possible_dates:
                group_date_var = self._model.addVar(
                    f"{GROUP_ID}-{group.id}-{DATE_ID}-{date[0]}-{date[1]}-{date[2]}",
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
                            (group.id, evaluator.id, date[0], date[1], date[2])
                        ]
                        for evaluator in self._evaluators
                        if (group.id, evaluator.id, date[0], date[1], date[2])
                        in self._decision_variables
                    )
                    / len(self._evaluators),
                    name=f"{GROUP_ID}-{group.id}-{DATE_ID}-{date[0]}-{date[1]}\
                    -{date[2]}",
                )
            self._model.addCons(
                scip.quicksum(group_date_vars.values()) == 1,
                name=f"{GROUP_ID}-{group.id}",
            )

    def _add_min_max_assignment_constraints(self, group):
        """
        Adds constraints to ensure each group is assigned to at least
        a minimum and at most a maximum number of evaluators.

        Parameters:
        -----------
        group : Group
            A group that needs an evaluator.
        """
        group_possible_dates = [
            (week, day, hour)
            for (g, t, week, day, hour) in self._result_tutors
            if g == group.id
        ]
        if len(group_possible_dates) > 0:
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
                name=f"max-assign-{GROUP_ID}-{group.id}",
            )

            self._model.addCons(
                scip.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[0] == group.id
                )
                >= min_evaluators,
                name=f"min-assign-{GROUP_ID}-{group.id}",
            )

    def add_evaluator_minimization_constraints(self):
        """
        Adds constraints to minimize the attendance days of evaluators.
        """
        for evaluator_id, week, day in self._evaluator_day_vars:
            self._model.addCons(
                self._evaluator_day_vars[(evaluator_id, week, day)]
                >= scip.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[1] == evaluator_id and var[2] == week and var[3] == day
                )
                / len(self._available_dates)
            )

    def add_evaluator_group_assignment_constraints(self):
        """
        Adds constraints to ensure evaluators are assigned all
        groups present on a given day, up to a maximum of 5 groups per week.
        """
        for evaluator in self._evaluators:
            self._add_weekly_group_limit_constraint(evaluator)

    def _add_weekly_group_limit_constraint(self, evaluator):
        """
        Adds a constraint to ensure an evaluator is not
        assigned more than 5 groups per week.

        Parameters:
        -----------
        evaluator : Evaluator
            An evaluator available for assignment.
        """
        weeks = set(date.week for date in self._available_dates)
        for week in weeks:
            self._model.addCons(
                scip.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[1] == evaluator.id and var[2] == week
                )
                <= 5,
                name=f"max-5-groups-week-{EVALUATOR_ID}-{evaluator.id}-{week}",
            )

    def define_objective(self):
        """
        Defines the objective of minimizing the number of days evaluators attend.
        """
        self._model.setObjective(
            scip.quicksum(
                self._evaluator_day_vars[(evaluator_id, week, day)]
                for (evaluator_id, week, day) in self._evaluator_day_vars
            ),
            "minimize",
        )

    def solve(self):
        """
        Solves the linear programming model.

        Returns:
        --------
        list
            List of activated decision variables.
        """
        self._configure_solver()

        self.create_decision_variables()
        self.add_group_assignment_constraints()
        self.add_evaluator_minimization_constraints()
        self.add_evaluator_group_assignment_constraints()
        self.define_objective()

        self._model.optimize()

        return self._get_results()

    def _configure_solver(self):
        """
        Configures the solver with appropriate parameters.
        """
        self._model.setRealParam(
            "limits/time", 600
        )  # Limit the solving time to 600 seconds (10 minutes)
        self._model.setIntParam(
            "limits/solutions", 100
        )  # Limit the number of solutions
        self._model.setRealParam("limits/gap", 0.01)  # Set an optimality gap of 1%
        self._model.setIntParam("presolving/maxrounds", 0)  # Disable presolving
        self._model.setIntParam(
            "branching/random/priority", 100
        )  # Use a random branching strategy

    def _get_results(self):
        """
        Retrieves and prints the results from the solver.

        Returns:
        --------
        list
            List of activated decision variables.
        """
        print("Status:", self._model.getStatus())
        print("Optimal objective value:", self._model.getObjVal())

        result = []
        print("Activated decision variables:")
        for var in self._decision_variables:
            if self._model.getVal(self._decision_variables[var]) > 0:
                print(f"Variable {var} (Group, Evaluator, Week, Day, Hour): {var}")
                result.append((f"{GROUP_ID}-{var[0]}", f"{EVALUATOR_ID}-{var[1]}", f"{DATE_ID}-{var[2]}-{var[3]}-{var[4]}"))

                group_id, week, day, hour, evaluator_id = var
                group = next(g for g in self._groups if g.id == group_id)
                group.state.assign_date(DeliveryDate(week, day, hour))

        print("\nAdditional activated variables (Evaluator, Week, Day):")
        for var in self._evaluator_day_vars:
            if self._model.getVal(self._evaluator_day_vars[var]) > 0:
                print(f"Additional variable {var}")

        return result
