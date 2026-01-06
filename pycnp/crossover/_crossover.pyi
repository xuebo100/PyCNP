from pycnp._pycnp import Graph

# Re-export constants for backwards compatibility
DBX: str
IRR: str
RSC: str

def double_backbone_based_crossover(
    orig_graph: Graph,
    parents: list[set[int]],
    seed: int,
) -> Graph:
    """
    Double Backbone Based (DBX) crossover operator.

    Identifies common nodes between parent solutions (the "backbone") and
    constructs an offspring by preserving these common nodes and probabilistically
    inheriting others.
    """
    ...

def inherit_repair_recombination(
    orig_graph: Graph,
    parents: list[set[int]],
    seed: int,
) -> Graph:
    """
    Inherit-Repair-Recombination (IRR) crossover operator.

    Uses three parents to create offspring through a process of inheritance
    followed by repair operations to maintain feasibility.
    """
    ...

def reduce_solve_combine(
    orig_graph: Graph,
    parents: list[set[int]],
    search: str = "CHNS",
    beta: float = 0.9,
    seed: int = ...,
) -> Graph:
    """
    Reduce-Solve-Combine (RSC) crossover operator.

    Reduces common nodes between parents, solves the reduced subproblem
    via local search, and combines the results to form an offspring.
    """
    ...
