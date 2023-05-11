from __future__ import annotations


def greedy_insert(solution, rng, data: ProblemData, **kwargs):
    """
    Insert the unassigned customers into the best place, one-by-one.
    """
    rng.shuffle(solution.unassigned)

    while solution.unassigned:
        customer = solution.unassigned.pop()
        solution.opt_insert(data, customer)

    solution.update_cost(data)

    return solution
