import networkx as nx
from src.algorithms.delivery_solver import DeliverySolver
from src.constants import GROUP_ID, EVALUATOR_ID, DATE_ID


class DeliveryFlowSolver(DeliverySolver):

    def __init__(self, groups, tutors, formatter, available_dates, evaluators):
        super().__init__(groups, tutors, formatter, available_dates)
        self._evaluators = evaluators

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

    def _create_date_edges(self, nodes: list, possible_dates: list, prefix_node: str):
        """
        Based on a list of nodes, and possible dates
        its create the edges based on items from the intersection
        like group-1 -(1,1)-> date-hr
        """
        edges = []
        for node in nodes:
            shared_dates = node.filter_dates(possible_dates)
            for date in shared_dates:
                date_label = date.label()
                edges.append(
                    (
                        f"{prefix_node}-{node.id}",
                        f"{DATE_ID}-{date_label}",
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
            edges.append(
                (f"{DATE_ID}-{date_label}", "t", {"capacity": capacity, "cost": 1})
            )

        return edges

    def _create_evaluators_week_edges(self, evaluators):
        """
        Based on evaluators it creates one edge between
        evaluator and its week
        """
        edges = []
        for evaluator in evaluators:
            dates = evaluator.available_dates
            weeks = set(d.week for d in dates)
            for week in weeks:
                week_edge = (
                    f"evaluator-{evaluator.id}",
                    f"{DATE_ID}-{week}-evaluator-{evaluator.id}",
                    {"capacity": 5, "cost": 1},
                )
                edges.append(week_edge)
                for date in dates:
                    if date.week == week:
                        edge = (
                            f"{DATE_ID}-{week}-evaluator-{evaluator.id}",
                            f"{DATE_ID}-{date.label()}",
                            {"capacity": 1, "cost": 1},
                        )
                        edges.append(edge)

        return edges

    def _filter_unassigned_dates(self, groups, evaluators):
        """
        When the evaluators contains the dates already assigned
        Tutors and groups need to filter so that they can match with
        evaluators day.

        This function is in charge of removed unassigned dates from the evaluators 
        """
        for group in groups:
            for evaluator in evaluators:
                if group.is_tutored_by(evaluator.id):
                    assigned_dates = evaluator.assigned_dates
                    group.remove_dates(assigned_dates)

    def groups_assignment_flow(self):
        """
        Creates a directed graph based on the different edges
        for groups flow
        """
        sources_edges = self._create_source_edges(self._groups, 1, GROUP_ID)
        date_edges = self._create_date_edges(
            self._groups, self._available_dates, GROUP_ID
        )
        sink_edges = self._create_sink_edges(self._available_dates, 1)

        graph = nx.DiGraph()
        graph.add_edges_from(sources_edges)
        graph.add_edges_from(date_edges)
        graph.add_edges_from(sink_edges)
        return graph

    def _filter_evaluators_dates(self):
        dates = []
        for e in self._evaluators:
            dates += e.filter_dates(self._available_dates)

        return dates

    def evaluators_assignment_flow(self):

        mutual_dates = self._filter_evaluators_dates()
        sources_edges = self._create_source_edges(self._evaluators, 35, EVALUATOR_ID)
        weeks_date_edges = self._create_evaluators_week_edges(self._evaluators)
        sink_edges = self._create_sink_edges(mutual_dates, 2)

        graph = nx.DiGraph()
        graph.add_edges_from(sources_edges)
        graph.add_edges_from(weeks_date_edges)
        graph.add_edges_from(sink_edges)
        return graph


    def _assign_evaluators_results_recursive(self, list_of_keys, result):
        if "t" in result[list_of_keys[0]]:
            value = result[list_of_keys[0]]
            if value["t"] > 0:
                return [list_of_keys[0]] 
            else:
                return []
        else:
            for i in list_of_keys:
                dates = list(result[i].keys())
                dates_left = self._assign_evaluators_results_recursive(dates[len(dates)//2:], result) 
                dates_right = self._assign_evaluators_results_recursive(dates[:len(dates)//2], result)
                
                return dates_left + dates_right

    def _assign_evaluators_results(self, result):
        for evaluator in self._evaluators:
            weeks = list(result[f"{EVALUATOR_ID}-{evaluator.id}"].keys())
            dates_left = self._assign_evaluators_results_recursive(weeks[len(weeks)//2:], result) 
            dates_right = self._assign_evaluators_results_recursive(weeks[:len(weeks)//2], result)
            final_dates = dates_left + dates_right
            evaluator.assign_dates(final_dates)


    def _filter_evaluators_tutors_date(self, evalutors, tutors):
        pass

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

        evaluator_graph = self.evaluators_assignment_flow()
        max_flow_min_cost_evaluators = self._max_flow_min_cost(evaluator_graph)

        self._assign_evaluators_results(max_flow_min_cost_evaluators)

        # filtro fechas de evaluadores con los tutores restantes
        #self._filter_evaluators_tutors_date(self._tutors, self._evaluators)
        self._filter_unassigned_dates(self._groups, self._evaluators)


        # Hago el grafo de los tutores y filtro los resultados
        #evaluator_graph = self.evaluators_assignment_flow()
        #self._filter_unassigned_dates(self._groups, self._tutors)

        # Hago el grafo de los alumnos
        groups_graph = self.groups_assignment_flow()
        max_flow_min_cost_groups = self._max_flow_min_cost(groups_graph)

        assignment_result = self._formatter.format_result(
            max_flow_min_cost_groups, self._groups, self._evaluators
        )

        return assignment_result
