import pandas as pd
from src.io.input_formatter import InputFormatter
from src.algorithms.delivery_flow_solver import DeliveryFlowSolver
from src.io.output.output_formatter import OutputFormatter

groups_df = pd.read_csv("db/equipos.csv")
tutors_df = pd.read_csv("db/tutores.csv")

formatter = InputFormatter(groups_df, tutors_df)
groups, tutors, evaluators, possible_dates = formatter.get_data()
# for tutor in tutors:
#     print(f"tutor {tutor.id}, name {tutor.name}")

# DeliveryFlowSolver(groups, tutors, formatter, available_dates, evaluators)
flow_solver = DeliveryFlowSolver(
    groups, tutors, OutputFormatter(), possible_dates, evaluators
)

result = flow_solver.solve()
print(f"Flow Solver result: {result}")
groups_result = result.groups
for group in groups_result:
    print(
        f"group {group.id}, tutor {group.tutor.id}, \
        delivery_date {result.delivery_date_group(group)}"
    )

evaluators_result = result.evaluators
for evaluator in evaluators_result:
    print(
        f"evaluator {evaluator.id}, count delivery_date \
        {len(result.delivery_date_evaluator(evaluator))}"
    )
    for date in result.delivery_date_evaluator(evaluator):
        print(f"evaluator {evaluator.id}, delivery_date {date}")
