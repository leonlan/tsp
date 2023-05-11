from time import perf_counter

import elkai
from alns.Result import Result
from alns.Statistics import Statistics

from tsp.classes import Solution


def solve_lkh(seed, data, max_iterations=1000, **kwargs):
    """
    Solves the TSP without appointment scheduling.
    """
    stats = Statistics()
    stats.collect_runtime(perf_counter())

    tour = elkai.solve_int_matrix(data.distances, runs=max_iterations)
    tour.remove(0)  # remove depot

    solution = Solution.from_tour(data, tour)
    stats.collect_objective(solution.cost)
    stats.collect_runtime(perf_counter())

    return Result(solution, stats)
