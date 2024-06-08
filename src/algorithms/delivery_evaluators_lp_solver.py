import pyscipopt as scip
from src.constants import DATE_ID, EVALUATOR_ID, GROUP_ID, TUTOR_ID
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

    def __init__(self, dates, groups, tutors, evaluators):
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
        self._result_tutors = {}
        self._groups = groups
        self._tutors = tutors
        self._evaluators = evaluators
        self._available_dates = dates
        self._decision_variables = {}
        self._evaluator_day_vars = {}
        self._tutor_day_vars = {}
        self._model = scip.Model()
        self._model.setIntParam("display/verblevel", 0)

    def create_decision_variables(self):
        """
        Creates decision variables for the assignment of evaluators to groups.
        """
        for group in self._groups:
            tutor = group.tutor
            mutual_available_dates = [
                (date.week, date.day, date.hour)
                for date in group.state.available_dates
                if any(
                    t_date.week == date.week
                    and t_date.day == date.day
                    and date.hour == t_date.hour
                    for t_date in tutor.state.available_dates
                )
            ]
            if len(mutual_available_dates) > 0:
                for week, day, hour in mutual_available_dates:
                    var_name = f"{GROUP_ID}-{group.id}-{TUTOR_ID}-{tutor.id}-\
                        {DATE_ID}-{week}-{day}-{hour}"
                    self._result_tutors[(group.id, tutor.id, week, day, hour)] = (
                        self._model.addVar(var_name, vtype="B", obj=0, lb=0, ub=1)
                    )

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
        if len(group_possible_dates) > 0:
            mutual_available_dates = [
                (week, day, hour)
                for (g, t, week, day, hour) in group_possible_dates
                for e_date in evaluator.available_dates
                if day == e_date.day and week == e_date.week and hour == e_date.hour
            ]

            if len(mutual_available_dates) > 0:
                if evaluator.id != group.tutor.id:
                    for week, day, hour in mutual_available_dates:
                        var_name = f"{GROUP_ID}-{group.id}-{TUTOR_ID}-{group.tutor.id}-\
                            {EVALUATOR_ID}-{evaluator.id}-{DATE_ID}-{week}-{day}-{hour}"
                        self._decision_variables[
                            (group.id, group.tutor.id, evaluator.id, week, day, hour)
                        ] = self._model.addVar(var_name, vtype="B", obj=0, lb=0, ub=1)
                        if (evaluator.id, week, day) not in self._evaluator_day_vars:
                            day_var_name = (
                                f"{EVALUATOR_ID}-{evaluator.id}-{DATE_ID}-{week}-{day}"
                            )
                            self._evaluator_day_vars[(evaluator.id, week, day)] = (
                                self._model.addVar(
                                    day_var_name, vtype="B", obj=0, lb=0, ub=1
                                )
                            )
                        if (group.tutor.id, week, day) not in self._tutor_day_vars:
                            day_var_name = (
                                f"{TUTOR_ID}-{group.tutor.id}-{DATE_ID}-{week}-{day}"
                            )
                            self._tutor_day_vars[(group.tutor.id, week, day)] = (
                                self._model.addVar(
                                    day_var_name, vtype="B", obj=0, lb=0, ub=1
                                )
                            )

    def tutor_max_groups_per_date_restriction(self):
        """
        Adds the restriction that each tutor can have at most 5 groups per day.

        Parameters:
        -----------
        num_week : int
            The week number for which the restrictions are being added.
        """
        for tutor in self._tutors:
            for date in self._available_dates:
                variables = [
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[3] == date.week and var[4] == date.day and var[1] == tutor.id
                ]
                if len(variables) > 0:
                    self._model.addCons(scip.quicksum(variables) <= 5)

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
                    if var[3] == week and var[4] == day and var[1] == tutor_id
                )
                / len(self._available_dates)
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
        group_possible_dates = [
            (week, day, hour)
            for (g, t, week, day, hour) in self._result_tutors
            if g == group.id
        ]
        if len(group_possible_dates) > 0:
            group_date_vars = {}
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
                            (
                                group.id,
                                group.tutor.id,
                                evaluator.id,
                                date[0],
                                date[1],
                                date[2],
                            )
                        ]
                        for evaluator in self._evaluators
                        if (
                            group.id,
                            group.tutor.id,
                            evaluator.id,
                            date[0],
                            date[1],
                            date[2],
                        )
                        in self._decision_variables
                    )
                    / len(self._evaluators),
                    name=f"{GROUP_ID}-{group.id}-{DATE_ID}-{date[0]}-\
                        {date[1]}-{date[2]}",
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
        number_available_evaluators = {}
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
                number_available_evaluators[date] = available_evaluators

            variables = [
                self._decision_variables[var]
                for var in self._decision_variables
                if var[0] == group.id
            ]
            if len(variables) > 0:
                self._model.addCons(
                    scip.quicksum(variables) <= 4,
                    name=f"max-assign-{GROUP_ID}-{group.id}",
                )

            variables = [
                self._decision_variables[var]
                for var in self._decision_variables
                if var[0] == group.id
            ]
            if len(variables) > 0:

                self._model.addCons(
                    scip.quicksum(variables) >= 1,
                    name=f"min-assign-{GROUP_ID}-{group.id}",
                )

    def add_unique_group_per_date_constraint(self):
        """
        Adds the constraint that each date can have only one group assigned.
        """
        dates = set(
            (week, day, hour) for _, _, _, week, day, hour in self._decision_variables
        )
        for date in dates:
            variables = [
                self._decision_variables[var]
                for var in self._decision_variables
                if (var[3], var[4], var[5]) == date
            ]
            if variables:
                self._model.addCons(
                    scip.quicksum(variables) <= 1, name=f"unique-group-date-{date}"
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
                    if var[2] == evaluator_id and var[3] == week and var[4] == day
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
                    if var[2] == evaluator.id and var[3] == week
                )
                <= 5,
                name=f"max-10-groups-week-{EVALUATOR_ID}-{evaluator.id}-{week}",
            )

    def define_objective(self):
        """
        Defines the objective of minimizing the number of days evaluators attend.
        """
        self._model.setObjective(
            scip.quicksum(
                week * self._evaluator_day_vars[(evaluator_id, week, day)]
                for (evaluator_id, week, day) in self._evaluator_day_vars
            )
            + scip.quicksum(
                week * self._tutor_day_vars[(tutor_id, week, day)]
                for (tutor_id, week, day) in self._tutor_day_vars
            ),
            "minimize",
        )

    def create_auxiliary_variables(self):
        """
        Creates auxiliary variables for the number of assignments per evaluator.
        """
        self._evaluator_assignment_vars = {}
        for evaluator in self._evaluators:
            var_name = f"{EVALUATOR_ID}-{evaluator.id}-assignments"
            self._evaluator_assignment_vars[evaluator.id] = self._model.addVar(
                var_name, vtype="I", obj=0, lb=0
            )

    def add_assignment_count_constraints(self):
        """
        Adds constraints to count the number of assignments per evaluator.
        """
        for evaluator in self._evaluators:
            self._model.addCons(
                self._evaluator_assignment_vars[evaluator.id]
                == scip.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[2] == evaluator.id
                ),
                name=f"count-assignments-{EVALUATOR_ID}-{evaluator.id}",
            )

    def add_balance_constraints(self):
        """
        Adds constraints to balance the workload among evaluators.
        """
        for i, evaluator_i in enumerate(self._evaluators):
            for j, evaluator_j in enumerate(self._evaluators):
                if i < j:
                    self._model.addCons(
                        self._evaluator_assignment_vars[evaluator_i.id]
                        - self._evaluator_assignment_vars[evaluator_j.id]
                        <= 5,  # Balance threshold
                        name=f"balance-{EVALUATOR_ID}-{evaluator_i.id}-\
                            {evaluator_j.id}",
                    )
                    self._model.addCons(
                        self._evaluator_assignment_vars[evaluator_j.id]
                        - self._evaluator_assignment_vars[evaluator_i.id]
                        <= 5,  # Balance threshold
                        name=f"balance-{EVALUATOR_ID}-{evaluator_j.id}-\
                            {evaluator_i.id}",
                    )

    def solve(self):
        """
        Solves the linear programming model.

        Returns:
        --------
        list
            List of activated decision variables.
        """
        # self._configure_solver()

        self.create_decision_variables()
        # Nueva función para crear variables auxiliares
        self.create_auxiliary_variables()

        self.add_group_assignment_constraints()
        self.add_evaluator_minimization_constraints()
        self.add_evaluator_group_assignment_constraints()
        self.tutor_max_groups_per_date_restriction()
        self.add_unique_group_per_date_constraint()
        # Nueva función para añadir restricciones de conteo
        self.add_assignment_count_constraints()
        self.add_balance_constraints()
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
                print(
                    f"Variable {var} (Group, Tutor, Evaluator, Week, Day, Hour): {var}"
                )
                result.append(
                    (
                        f"{GROUP_ID}-{var[0]}",
                        f"{EVALUATOR_ID}-{var[2]}",
                        f"{DATE_ID}-{var[3]}-{var[4]}-{var[5]}",
                    )
                )

                group_id, tutor_id, evaluator_id, week, day, hour = var
                group = next(g for g in self._groups if g.id == group_id)
                group.assign_date(DeliveryDate(week, day, hour))

        print("\nAdditional activated variables (Evaluator, Week, Day):")
        for var in self._evaluator_day_vars:
            if self._model.getVal(self._evaluator_day_vars[var]) > 0:
                print(f"Additional variable {var}")

        return result
