import networkx as nx
from src.algorithms.delivery_solver import DeliverySolver


class DeliveryFlowSolver(DeliverySolver):

    def __init__(self, groups, tutors, formatter, avaliable_dates, evaluators):
        super().__init__(groups, tutors, formatter, avaliable_dates)
        self._evaluators = evaluators

    def _create_source_edges(self, nodes: list, capacity: int) -> list:
        """
        Based on a list of nodes, and a base capacity
        its create the edges for s -(capacity,1)-> node
        """
        edges = []
        for node in nodes:
            edge = ("s", f"{node.id}", {"capacity": capacity, "cost": 1})
            edges.append(edge)

        return edges

    def _create_date_edges(self, nodes: list, possible_dates: list):
        """
        Based on a list of nodes, and possible dates
        its create the edges based on items from the intersection
        like g1 -(1,1)-> date-hr
        """
        edges = []
        for node in nodes:
            shared_dates = node.filter_dates(possible_dates)
            for date in shared_dates:
                date_label = date.label()
                edges.append(
                    (
                        f"{node.id}",
                        date_label,
                        {"capacity": 1, "cost": 1},
                    )
                )
        return edges

    def _create_sink_edges(self, possible_dates: list, capacity: int):
        """
        Based on a list of possible dates
        its create the edges to sink node
        like date-hr -(1,1)-> t
        """
        edges = []
        for date in possible_dates:
            date_label = date.label()
            edges.append((date_label, "t", {"capacity": capacity, "cost": 1}))

        return edges

    def _create_evaluators_week_edges(self, evaluators):
        """
        Based on evaluators it creates one edge between
        evaluator and its week
        """
        edges = []
        for evaluator in evaluators:
            dates = evaluator.avaliable_dates
            weeks = set(d.week for d in dates)
            for week in weeks:
                week_edge = (
                    f"{evaluator.id}",
                    f"{week}-{evaluator.id}",
                    {"capacity": 5, "cost": 1},
                )
                edges.append(week_edge)
                for date in dates:
                    if date.week == week:
                        edge = (
                            f"{week}-{evaluator.id}",
                            date.label(),
                            {"capacity": 1, "cost": 1},
                        )
                        edges.append(edge)

        return edges

    def _filter_unassigned_dates(self, group, evaluator):
        if group.is_tutored_by(evaluator.id):
            assigned_dates = evaluator.assigned_dates
            group.remove_dates(assigned_dates)

    def groups_assigment_flow(self):
        """
        Creates a directed graph based on the different edges
        """
        sources_edges = self._create_source_edges(self._groups, 1)
        date_edges = self._create_date_edges(self._groups, self._avaliable_dates)
        sink_edges = self._create_sink_edges(self._avaliable_dates, 1)

        graph = nx.DiGraph()
        graph.add_edges_from(sources_edges)
        graph.add_edges_from(date_edges)
        graph.add_edges_from(sink_edges)
        return graph

    def _filter_final_dates(self):
        dates = []
        for e in self._evaluators:
            dates += e.filter_dates(self._avaliable_dates)

        return dates

    def evaluators_assigment_flow(self):

        mutual_dates = self._filter_final_dates()
        sources_edges = self._create_source_edges(self._evaluators, 35)
        weeks_date_edges = self._create_evaluators_week_edges(self._evaluators)
        sink_edges = self._create_sink_edges(mutual_dates, 2)

        graph = nx.DiGraph()
        graph.add_edges_from(sources_edges)
        graph.add_edges_from(weeks_date_edges)
        graph.add_edges_from(sink_edges)
        return graph

    def _assign_evaluators_results(self, result):
        for evaluator in self._evaluators:
            weeks = result[evaluator.id]
            for key, value in weeks.items():
                if value > 0:
                    days = result[key]
                    for date, date_value in days.items():
                        if date_value == 1:
                            evaluator.assign_date(date)

    def _max_flow_min_cost(self, graph: nx.DiGraph):
        """
        Based on a directed graph its calculates the max flow min cost of
        that flow graph
        """
        max_flow_min_cost_dic = nx.max_flow_min_cost(
            graph, "s", "t", capacity="capacity", weight="cost"
        )

        return max_flow_min_cost_dic

    def solve(self):

        evaluator_graph = self.evaluators_assigment_flow()
        max_flow_min_cost_evaluators = self._max_flow_min_cost(evaluator_graph)

        self._assign_results(max_flow_min_cost_evaluators)
        self._filter_unassigned_dates(self._groups, self._evaluators)

        groups_graph = self.groups_assigment_flow()
        max_flow_min_cost_groups = self._max_flow_min_cost(groups_graph)

        # assignment_result = self.formatter.format_delivery_result(max_flow_min_cost_groups,self._tutors, self._groups, self._evaluators)

        return assignment_result
