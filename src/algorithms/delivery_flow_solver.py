import networkx as nx
from src.algorithms.delivery_solver import DeliverySolver
from src.constants import GROUP_ID, EVALUATOR_ID, DATE_ID


class DeliveryFlowSolver(DeliverySolver):

    def __init__(self, groups, tutors, formatter, available_dates, evaluators):
        super().__init__(groups, tutors, formatter, available_dates)
        self._evaluators = evaluators

    # Common methods
    def _create_source_edges(
        self, nodes: list, capacity: int, prefix_node: str
    ) -> list:
        """
        Based on a list of nodes, and a base capacity
        its create the edges for s -(capacity,1)-> node
        """
        edges = []
        for node in nodes:
            edge = ("s", f"{prefix_node}-{node.id}", {"capacity": capacity, "cost": 1})
            edges.append(edge)

        return edges

    def _create_sink_edges(self, nodes: list, capacity: int, node_prefix):
        """
        Based on a list of possible dates
        its create the edges to sink node
        """
        edges = []
        for node in nodes:
            edges.append(
                (f"{node_prefix}-{node}", "t", {"capacity": capacity, "cost": 1})
            )

        return edges

    # Group edges methods
    def _create_group_date_edges(self, clean_results):
        """
        With the results already cleaned, and edge from a group to a date should be created
        if that date contains the same week as the clean_results has for a particular group_id
        """
        sources_edges = self._create_source_edges(self._groups, 1, GROUP_ID)
        edges = []
        final_dates = []
        for group in self._groups:
            week, evaluator_id = clean_results[f"{GROUP_ID}-{group.id}"]
            evaluators_dates = self._get_evaluator_dates(evaluator_id)
            group.filter_dates(evaluators_dates)
            for date in group.available_dates():
                if date.week == week:
                    date_label = date.label()
                    cost_date = group.cost_of_date(date)
                    edges.append(
                        (
                            f"{GROUP_ID}-{group.id}",
                            f"{DATE_ID}-{date_label}",
                            {"capacity": 1, "cost": cost_date},
                        )
                    )
                    final_dates.append(date_label)
        sink_edges = self._create_sink_edges(list(set(final_dates)), 1, DATE_ID)
        return edges + sink_edges + sources_edges

    def _filter_groups_dates(self, mutual_dates):
        """
        Remove all the dates that won't be used for creating edges
        returning the labels of each one that will be considered
        """
        dates = []
        for group in self._groups:
            dates += group.filter_dates(mutual_dates)

        return list(set(dates))

    def _get_groups_id_with_mutual_dates(self, week, dates, evaluator_id):
        """
        Search for at least mutual date between a group and an evaluator,
        the evaluator can't be the group's tutor.
        """
        groups = []
        for group in self._groups:
            if group.is_tutored_by(evaluator_id) is False:
                group_dates = list(d.label() for d in group.available_dates())
                weeks_dates = list(filter(lambda x: x.split("-")[0] == week, dates))
                mutual_dates = list(set(group_dates) & set(weeks_dates))
                if len(mutual_dates) > 0:
                    cost = group.cost_of_week(week)
                    groups.append((group.id, cost))
        return groups

    # Evaluators methods

    def _create_evaluators_edges(self):
        """
        Based on evaluators it creates one edge between
        evaluator and its week, it also search for groups with mutual dates
        and connect that week node to the group as they share at least one date.
        """
        sources_edges = self._create_source_edges(self._evaluators, 35, EVALUATOR_ID)
        edges = []
        all_group_ids = []
        for evaluator in self._evaluators:
            weeks_checked = []
            evaluador_dates = [d.label() for d in evaluator.available_dates]
            for date in evaluador_dates:
                week = date.split("-")[0]
                if week not in weeks_checked:
                    weeks_checked.append(week)
                    week_edge = (
                        f"evaluator-{evaluator.id}",
                        f"{DATE_ID}-{week}-evaluator-{evaluator.id}",
                        {"capacity": 5, "cost": 1},
                    )
                    edges.append(week_edge)
                    groups_info = self._get_groups_id_with_mutual_dates(
                        week, evaluador_dates, evaluator.id
                    )

                    for group in groups_info:
                        if group[0] not in all_group_ids:
                            all_group_ids.append(group[0])

                        edge = (
                            f"{DATE_ID}-{week}-evaluator-{evaluator.id}",
                            f"{GROUP_ID}-{group[0]}",
                            {"capacity": 1, "cost": group[1]},
                        )
                        edges.append(edge)
        sink_edges = self._create_sink_edges(all_group_ids, 1, GROUP_ID)
        return sources_edges + edges + sink_edges

    def _filter_evaluators_dates(self):
        """
        Collects all the dates labels based in the intersection of each evaluator
        """
        dates = []
        for e in self._evaluators:
            dates += e.filter_dates(self._available_dates)

        return list(set(dates))

    def _clean_evaluators_results(self, results):
        """
        With the evaluators resuts, it reduces the values just to have the important info
        such as group, week to evaluate, evaluator id that evaluates that group
        """
        cleaned_results = {}
        for evaluator in self._evaluators:
            evaluator_key = f"{EVALUATOR_ID}-{evaluator.id}"
            evaluator_results = results[evaluator_key]

            for week, week_value in evaluator_results.items():
                week_num = int(week.split("-")[1])
                week_key = f"week-{week_num}"

                if week_value > 0:

                    for group, group_value in results[week_key].items():
                        if group_value > 0:
                            cleaned_results[group] = (int(week_num), evaluator.id)

        return cleaned_results

    def _get_evaluator_dates(self, evaluator_id):
        """
        Collect of the evaluators dates labels based on an id
        """
        for evaluator in self._evaluators:
            if evaluator.id == evaluator_id:
                return [d.label() for d in evaluator._available_dates]

        return []

    # Graph methods
    def _max_flow_min_cost(self, graph: nx.DiGraph):
        """
        It calculates the max flow min cost of directed graph
        """
        max_flow_min_cost_dic = nx.max_flow_min_cost(
            graph, "s", "t", capacity="capacity", weight="cost"
        )

        return max_flow_min_cost_dic

    def solve(self):
        """
        Based on mutual dates between the evaluators, tutors and groups

        First, we create a graph to solve max flow min cost for evaluators,
        in this graph we create an edge between an evaluator and a week where the evaluator can evaluate
        Then, those weeks have edges to each group where each group has at least one common date in that week with
        the evaluator
        The result of this graph can be intrepreted as 'Which evaluator evaluates a group on week n'

        After the first graph is completed, we clean the results to improve performance and create the groups edges.
        Each group contains and edge to all its dates related to a week.

        When the two graphs are completed, every group should have a date and an evaluator
        We also considered the cost inside each date base on the availability of that group in that date or week.

        """
        mutual_dates = self._filter_evaluators_dates()
        mutual_dates = self._filter_groups_dates(mutual_dates)

        evaluator_edges = self._create_evaluators_edges()
        e_graph = nx.DiGraph()
        e_graph.add_edges_from(evaluator_edges)
        max_flow_min_cost_evaluator = self._max_flow_min_cost(e_graph)

        clean_results = self._clean_evaluators_results(max_flow_min_cost_evaluator)

        groups_edges = self._create_group_date_edges(clean_results)
        g_graph = nx.DiGraph()
        g_graph.add_edges_from(groups_edges)
        max_flow_min_cost_groups = self._max_flow_min_cost(g_graph)

        # assignment_result = self._formatter.format_result(
        #    max_flow_min_cost_groups, self._groups, self._evaluators
        # )

        return max_flow_min_cost_evaluator, max_flow_min_cost_groups
