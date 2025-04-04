from copy import copy

from tsp.classes import Solution


def relocate(solution: Solution, rng, **kwargs):
    """
    Improves the current solution in-place using the relocate neighborhood.
    Each customer is selected once and optimally re-inserted.
    """
    customers = copy(solution.tour)

    for job in rng.choice(customers, len(customers), replace=False):
        solution.remove(job)
        solution.opt_insert(job)
