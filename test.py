#第一个实例
from pycnp import Model
from pycnp.MemeticSearch import MemeticSearchParams, VariablePopulationParams
from pycnp.stop import NoImprovement
from pycnp.visualization import visualize_graph

# Method 1: Use the modeling interface to construct a graph instance
model = Model()

# Add 20 nodes (0-19)
for i in range(20):
    model.add_node(i)

# Add 22 edges
edges = [
    (0, 4),
    (1, 4),
    (2, 4),
    (2, 6),
    (3, 4),
    (4, 9),
    (5, 9),
    (6, 9),
    (7, 9),
    (7, 11),
    (8, 9),
    (9, 14),
    (10, 14),
    (11, 14),
    (12, 14),
    (12, 16),
    (13, 14),
    (14, 19),
    (15, 19),
    (16, 19),
    (17, 19),
    (18, 19),
]

for u, v in edges:
    model.add_edge(u, v)

# Set the stopping criterion by restricting the number of generations
# without improvement to 20
stopping_criterion = NoImprovement(20)

# Set the problem type to CNP
problem_type = "CNP"
budget = 3
seed = 6

# Set the memetic search parameters
# - Explicitly choose RSC crossover, control internal search strategy
# and beta via reduce_params
memetic_params = MemeticSearchParams(
    search="CHNS",
    crossover="RSC",
    # is_problem_reduction=True,
    reduce_params={"search": "CHNS", "beta": 0.8},
    is_pop_variable=True,
    initial_pop_size=5,
)
pop_params = VariablePopulationParams(
    max_pop_size=20, increase_pop_size=3, max_idle_gens=20
)

# Solve the instance via VPMS
result = model.solve(
    problem_type,
    budget,
    stopping_criterion,
    seed,
    memetic_params,
    pop_params,
    display=True,
)

# Visualize the graph
visualize_graph(
    problem_data=model.problem_data,
    critical_nodes_set=result.best_solution,
)

#  第二个实例
# from math import floor

# from pycnp import Model, read
# from pycnp.MemeticSearch import MemeticSearchParams
# from pycnp.stop import MaxRuntime
# from pycnp.visualization import visualize_graph

# # Method 2: Use the file reading interface to load an existing instance
# problem_data = read("./Instances/DCNP/R1/Hi_tech.txt")
# model = Model.from_data(problem_data)

# # Set the problem type to DCNP, and restrict budget to no more than floor(0.10|V|)
# problem_type = "DCNP"
# budget = floor(0.1*problem_data.num_nodes())
# seed = 49

# # Set the stopping criterion by limit the maximal running time to 5 seconds
# stopping_criterion = MaxRuntime(5)
# memetic_params = MemeticSearchParams(
#     search="BCLS",
#     is_problem_reduction=True,
#     is_pop_variable=False,
#     initial_pop_size=5,
#     reduce_params={"search": "BCLS", "beta": 0.9}
# )

# # Solve the instance via FTMS
# result = model.solve(
#     problem_type,
#     budget,
#     stopping_criterion,
#     seed,
#     memetic_params,
#     hop_distance = 3, # Set the distance limit to 3
#     display=True
# )

# visualize_graph(
#     problem_data = problem_data,
#     critical_nodes_set = result.best_solution,
# )
