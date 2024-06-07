import pandas as pd
from src.model.formatter.input_formatter import InputFormatter
from src.algorithms.delivery_flow_solver import DeliveryFlowSolver
from src.model.formatter.output.output_formatter import OutputFormatter
from src.model.formatter.output.flow_formatter import FlowOutputFormatter

groups_df = pd.read_csv("db/equipos.csv")
tutors_df = pd.read_csv("db/tutores.csv")

formatter = InputFormatter(groups_df, tutors_df)
groups, tutors, evaluators, possible_dates = formatter.get_data()
# for tutor in tutors:
#     print(f"tutor {tutor.id}, name {tutor.name}")

# DeliveryFlowSolver(groups, tutors, formatter, available_dates, evaluators)
output_formatter = OutputFormatter()
flow_solver = DeliveryFlowSolver(
    groups, tutors, output_formatter, possible_dates, evaluators
)
graph = flow_solver.groups_assignment_flow()
result = flow_solver._max_flow_min_cost(graph)
ff = FlowOutputFormatter()
groups = ff._groups(result, flow_solver._groups)
for group in groups:
    print(f"group {group.id}, date {group.assigned_date()}\n")

# print("FLOW SOLVER RESULT: ", flow_solver._max_flow_min_cost(result))
# result = flow_solver.solve()
# print(f"Flow Solver result: {result}")
# groups_result = result.groups
# for group in groups_result:
#     print(f"group {group.id}, tutor {group.tutor.id}, delivery_date {result.delivery_date_group(group).label()}")

# evaluators_result = result.evaluators
# for evaluator in evaluators_result:
#     print(f"evaluator {evaluator.id}, count delivery_date {len(result.delivery_date_group(evaluator))}")
#     for date in result.delivery_date_evaluator(evaluator):
#         print(f"evaluator {evaluator.id}, delivery_date {date.label()}")
