import pyscipopt as scip
from src.assignments.adapters.result_context import ResultContext
from src.constants import DATE_ID, EVALUATOR_ID, GROUP_ID, TUTOR_ID
from src.model.period import TutorPeriod
from src.model.utils.delivery_date import DeliveryDate

GROUP = 0
TUTOR = 1
EVALUATOR = 2
WEEK = 3
DAY = 4
HOUR = 5
MAX_GROUPS_PER_WEEK = 5
MAX_GROUPS_PER_DAY = 5
MAX_DIF_EVALUATORS = 5


class DeliveryLPSolver:
    """
    Class to solve the problem of assigning evaluators to groups
    using linear programming.

    Attributes:
    -----------
    _evaluators : list
        List of available evaluators.
    _decision_variables : dict
        Decision variables for the assignment.
    _evaluator_day_vars : dict
        Variables to minimize the attendance days of evaluators.
    _model : scip.Model
        SCIP model to solve the problem.
    """

    def __init__(
        self, tutor_periods: list[TutorPeriod] = [], adapter=None, available_dates=[]
    ):
        """
        Initializes the class with tutor_periods and dates.

        Parameters:
        -----------
        available_dates : list
            List of available dates.
        tutor_periods : list
            List of tutors.
        """
        self._evaluators = self.create_evaluators(tutor_periods)
        self._tutors = self.get_tutors(tutor_periods)
        self._groups = self.get_all_groups(tutor_periods)
        self._available_dates = available_dates
        self._adapter = adapter
        self._decision_variables = {}
        self._evaluator_day_vars = {}
        self._model = scip.Model()
        self._model.setIntParam("display/verblevel", 0)

    def get_tutors(self, tutor_periods: list[TutorPeriod] = []):
        tutors = list(filter(lambda x: not x.is_evaluator(), tutor_periods))
        return tutors

    def get_all_groups(self, tutor_periods: list[TutorPeriod] = []):
        groups = []
        for t in tutor_periods:
            groups += t.groups
        return groups

    def create_evaluators(self, tutor_periods: list[TutorPeriod] = []):
        evaluators = list(filter(lambda x: x.is_evaluator(), tutor_periods))
        return evaluators

    def create_decision_variables(self):
        """
        Creates decision variables for the assignment of evaluators to groups.

        This function iterates over each group and evaluator, determining the
        possible dates where the group and its tutors can meet with the evaluator.
        For each valid combination of group, tutor, evaluator, and date, it
        creates a decision variable to represent whether the evaluator is assigned
        to the group on that date.
        """
        for tutor in self._tutors:
            for group in tutor.groups:
                group_tutor_possible_dates = self._find_common_dates(group, tutor)
                for evaluator in self._evaluators:
                    self._create_evaluator_decision_variables(
                        group, tutor, evaluator, group_tutor_possible_dates
                    )

    def _find_common_dates(self, group, tutor):
        """
        Finds common dates available for all tutors in the group.

        Parameters:
        -----------
        group : Group
            The group needing an evaluator.
        tutor : TutorPeriod
            The tutor associated with the group.

        Returns:
        --------
        list
            List of tuples representing common dates (week, day, hour).
        """
        return [
            (date.week, date.day, date.hour)
            for date in group.available_dates
            if any(
                t_date.week == date.week
                and t_date.day == date.day
                and date.hour == t_date.hour
                for t_date in tutor.available_dates
            )
        ]

    def _create_evaluator_decision_variables(
        self, group, tutor, evaluator, group_tutor_possible_dates
    ):
        """
        Creates decision variables for an evaluator's possible assignments.

        For each combination of group, evaluator, and possible date, it creates
        decision variables indicating whether the evaluator is assigned to the
        group on that date. It also creates day variables for both evaluators and
        tutors to track the days they are assigned.

        Parameters:
        -----------
        group : Group
            The group needing an evaluator.
        tutor : TutorPeriod
            The tutor associated with the group.
        evaluator : Evaluator
            The evaluator being considered for assignment.
        group_tutors_possible_dates : list
            List of dates (week, day, hour) where the group and tutors can meet.
        """
        group_tutor_evaluator_possible_dates = [
            (week, day, hour)
            for (week, day, hour) in group_tutor_possible_dates
            for e_date in evaluator.available_dates
            if day == e_date.day and week == e_date.week and hour == e_date.hour
        ]

        if group_tutor_evaluator_possible_dates:
            if evaluator.id() != tutor.id():
                for week, day, hour in group_tutor_evaluator_possible_dates:
                    self._create_decision_variable(
                        group, tutor.id(), evaluator, week, day, hour
                    )
                    self._create_evaluator_day_variable(evaluator, week, day)

    def _create_decision_variable(self, group, tutor_id, evaluator, week, day, hour):
        """
        Creates a single decision variable for a specific assignment.

        This function creates a binary decision variable indicating whether a
        particular evaluator is assigned to a group on a specific date.

        Parameters:
        -----------
        group : Group
            The group needing an evaluator.
        tutor_id : int
            ID of the tutor associated with the group.
        evaluator : TutorPeriod
            The evaluator being considered for assignment.
        week : int
            The week number of the assignment.
        day : int
            The day of the week of the assignment.
        hour : int
            The hour of the day of the assignment.
        """
        var_name = f"{GROUP_ID}-{group.id()}-{TUTOR_ID}-{tutor_id}-{EVALUATOR_ID}-{evaluator.id()}-{DATE_ID}-{week}-{day}-{hour}"
        self._decision_variables[
            (group.id(), tutor_id, evaluator.id(), week, day, hour)
        ] = self._model.addVar(var_name, vtype="B", obj=0, lb=0, ub=1)

    def _create_evaluator_day_variable(self, evaluator, week, day):
        """
        Creates a day variable for an evaluator.

        This function creates a binary variable indicating whether an evaluator
        is assigned to any group on a specific day.

        Parameters:
        -----------
        evaluator : Evaluator
            The evaluator being considered.
        week : int
            The week number of the assignment.
        day : int
            The day of the week of the assignment.
        """
        if (evaluator.id(), week, day) not in self._evaluator_day_vars:
            day_var_name = f"{EVALUATOR_ID}-{evaluator.id()}-{DATE_ID}-{week}-{day}"
            self._evaluator_day_vars[(evaluator.id(), week, day)] = self._model.addVar(
                day_var_name, vtype="B", obj=0, lb=0, ub=1
            )

    def add_group_assignment_constraints(self):
        """
        Adds group assignment constraints to the model.
        """
        for tutor in self._tutors:
            for group in tutor.groups:
                self._add_unique_date_constraint(group, tutor)
                self._add_assignment_constraints(group)

    def _add_unique_date_constraint(self, group, tutor):
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
            for (g, t, e, week, day, hour) in self._decision_variables
            if g == group.id()
        ]
        if group_possible_dates:
            group_date_vars = self._create_group_date_variables(
                group, group_possible_dates, tutor
            )
            self._model.addCons(
                scip.quicksum(group_date_vars.values()) == 1,
                name=f"{GROUP_ID}-{group.id()}",
            )

    def _create_group_date_variables(self, group, group_possible_dates, tutor):
        """
        Creates date variables for a group.

        This function creates binary variables for each possible date
        a group can be assigned to ensure they are mutually exclusive.

        Parameters:
        -----------
        group : Group
            The group needing an evaluator.
        group_possible_dates : list
            List of possible dates (week, day, hour) for the group.
        tutor : TutorPeriod
            The tutor associated with the group.
        Returns:
        --------
        dict
            Dictionary of created date variables.
        """
        group_date_vars = {}
        for date in group_possible_dates:
            group_date_var = self._model.addVar(
                f"{GROUP_ID}-{group.id()}-{DATE_ID}-{date[0]}-{date[1]}-{date[2]}",
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
                            group.id(),
                            tutor.id(),
                            evaluator.id(),
                            date[0],
                            date[1],
                            date[2],
                        )
                    ]
                    for evaluator in self._evaluators
                    if (
                        group.id(),
                        tutor.id(),
                        evaluator.id(),
                        date[0],
                        date[1],
                        date[2],
                    )
                    in self._decision_variables
                )
                / len(self._evaluators),
                name=f"{GROUP_ID}-{group.id()}-{DATE_ID}-{date[0]}-{date[1]}-{date[2]}",
            )
        return group_date_vars

    def _add_assignment_constraints(self, group):
        """
        Adds constraints to ensure each group is assigned to only one evaluator.

        Parameters:
        -----------
        group : Group
            A group that needs an evaluator.
        """
        variables = [
            self._decision_variables[var]
            for var in self._decision_variables
            if var[GROUP] == group.id()
        ]
        if variables:
            self._model.addCons(
                scip.quicksum(variables) == 1,
                name=f"min-assign-{GROUP_ID}-{group.id()}",
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
                if (var[WEEK], var[DAY], var[HOUR]) == date
            ]
            if variables:
                self._model.addCons(
                    scip.quicksum(variables) <= 1, name=f"unique-group-date-{date}"
                )

    def add_evaluator_minimization_constraints(self):
        """
        Adds constraints to minimize evaluator's attendance days.
        """
        for evaluator_id, week, day in self._evaluator_day_vars:
            self._model.addCons(
                self._evaluator_day_vars[(evaluator_id, week, day)]
                >= scip.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[EVALUATOR] == evaluator_id
                    and var[WEEK] == week
                    and var[DAY] == day
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
        Adds a constraint to limit the number of groups assigned to
        an evaluator per week.

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
                    if var[EVALUATOR] == evaluator.id() and var[WEEK] == week
                )
                <= MAX_GROUPS_PER_WEEK,
                name=f"max-10-groups-week-{EVALUATOR_ID}-{evaluator.id()}-{week}",
            )

    def define_objective(self):
        """
        Defines the objective of minimizing the number of days
        evaluators and tutors attend.
        """
        self._model.setObjective(
            scip.quicksum(
                week * self._evaluator_day_vars[(evaluator_id, week, day)]
                for (evaluator_id, week, day) in self._evaluator_day_vars
            ),
            "minimize",
        )

    def create_auxiliary_variables(self):
        """
        Creates auxiliary variables for the number of assignments per evaluator.
        """
        self._evaluator_assignment_vars = {}
        for evaluator in self._evaluators:
            var_name = f"{EVALUATOR_ID}-{evaluator.id()}-assignments"
            self._evaluator_assignment_vars[evaluator.id()] = self._model.addVar(
                var_name, vtype="I", obj=0, lb=0
            )

    def add_assignment_count_constraints(self):
        """
        Adds constraints to count the number of assignments per evaluator.
        """
        for evaluator in self._evaluators:
            self._model.addCons(
                self._evaluator_assignment_vars[evaluator.id()]
                == scip.quicksum(
                    self._decision_variables[var]
                    for var in self._decision_variables
                    if var[EVALUATOR] == evaluator.id()
                ),
                name=f"count-assignments-{EVALUATOR_ID}-{evaluator.id()}",
            )

    def add_balance_constraints(self):
        """
        Adds constraints to balance the workload among evaluators.
        """
        for i, evaluator_i in enumerate(self._evaluators):
            for j, evaluator_j in enumerate(self._evaluators):
                if i < j:
                    self._model.addCons(
                        self._evaluator_assignment_vars[evaluator_i.id()]
                        - self._evaluator_assignment_vars[evaluator_j.id()]
                        <= MAX_DIF_EVALUATORS,  # Balance threshold
                        name=f"balance-{EVALUATOR_ID}-{evaluator_i.id()}-{evaluator_j.id()}",
                    )
                    self._model.addCons(
                        self._evaluator_assignment_vars[evaluator_j.id()]
                        - self._evaluator_assignment_vars[evaluator_i.id()]
                        <= MAX_DIF_EVALUATORS,  # Balance threshold
                        name=f"balance-{EVALUATOR_ID}-{evaluator_j.id()}-{evaluator_i.id()}",
                    )

    def _find_substitutes_on_date(self, date, evaluator_id, tutor_id):
        substitutes = []
        for evaluator in self._evaluators:
            if (
                evaluator.is_avaliable(date.label())
                and evaluator.id() != evaluator_id
                and evaluator.id() != tutor_id
            ):
                substitutes.append(evaluator.id())
                evaluator.add_substitute_date(date)

        return substitutes

    def solve(self):
        """
        Solves the linear programming model.

        Returns:
        --------
        list
            List of activated decision variables.
        """
        self.create_decision_variables()
        self.create_auxiliary_variables()

        self.add_group_assignment_constraints()
        self.add_evaluator_minimization_constraints()
        self.add_evaluator_group_assignment_constraints()
        self.add_unique_group_per_date_constraint()
        self.add_assignment_count_constraints()
        self.add_balance_constraints()
        self.define_objective()
        self._model.optimize()

        if self._model.getStatus() == "optimal":
            return self._get_results()
        else:
            return None

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
        rounded_decision_vars = {
            var: round(self._model.getVal(self._decision_variables[var]))
            for var in self._decision_variables
        }
        rounded_evaluator_day_vars = {
            var: round(self._model.getVal(self._evaluator_day_vars[var]))
            for var in self._evaluator_day_vars
        }

        print("Activated decision variables:")
        for var in rounded_decision_vars:
            if rounded_decision_vars[var] > 0:
                print(
                    f"Variable {var} (Group, Tutor, Evaluator, Week, Day, Hour): {var}",
                    "val:",
                    self._model.getVal(self._decision_variables[var]),
                )
                # FIXME: no olvidarnos de los subtitutos, (pondria un bool para calcularlos o no)
                substitue = self._find_substitutes_on_date(
                    DeliveryDate(var[WEEK], var[DAY], var[HOUR]),
                    var[EVALUATOR],
                    var[TUTOR],
                )
                result.append(
                    (
                        f"{GROUP_ID}-{var[GROUP]}",
                        f"{EVALUATOR_ID}-{var[EVALUATOR]}",
                        f"{DATE_ID}-{var[WEEK]}-{var[DAY]}-{var[HOUR]}",
                    )
                )

                group_id, _, _, week, day, hour = var
                group = next(g for g in self._groups if g.id() == group_id)
                group.assign_date(DeliveryDate(week, day, hour))

        print("\nAdditional activated variables (Evaluator, Week, Day):")
        for var in rounded_evaluator_day_vars:
            if rounded_evaluator_day_vars[var] > 0:
                print(f"Additional variable {var}")

        result_context = ResultContext(
            type="linear",
            result=result,
        )

        assignment_result = self._adapter.adapt_results(result_context)

        return assignment_result
