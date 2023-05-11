from time import perf_counter
from itertools import combinations

from tsp.classes import Solution
from alns.Result import Result
from alns.Statistics import Statistics
import gurobipy as gp


def solve_milp(seed, data, grb_num_procs=1, **kwargs):
    stats = Statistics()
    stats.collect_runtime(perf_counter())

    m = gp.Model()

    capitals = list(range(data.distances.shape[0]))
    dist = {(c1, c2): data.distances[c1, c2] for c1, c2 in combinations(capitals, 2)}

    def subtourelim(model, where):
        # Callback - use lazy constraints to eliminate sub-tours
        if where == gp.GRB.Callback.MIPSOL:
            # make a list of edges selected in the solution
            vals = model.cbGetSolution(model._vars)
            selected = gp.tuplelist(
                (i, j) for i, j in model._vars.keys() if vals[i, j] > 0.5
            )
            # find the shortest cycle in the selected edge list
            tour = subtour(selected)
            if len(tour) < len(capitals):
                # add subtour elimination constr. for every pair of cities in subtour
                model.cbLazy(
                    gp.quicksum(model._vars[i, j] for i, j in combinations(tour, 2))
                    <= len(tour) - 1
                )

    def subtour(edges):
        # Given a tuplelist of edges, find the shortest subtour
        unvisited = capitals[:]
        cycle = capitals[:]  # Dummy - guaranteed to be replaced
        while unvisited:  # true if list is non-empty
            thiscycle = []
            neighbors = unvisited
            while neighbors:
                current = neighbors[0]
                thiscycle.append(current)
                unvisited.remove(current)
                neighbors = [j for i, j in edges.select(current, "*") if j in unvisited]
            if len(thiscycle) <= len(cycle):
                cycle = thiscycle  # New shortest subtour
        return cycle

    # Variables: is city 'i' adjacent to city 'j' on the tour?
    vars = m.addVars(dist.keys(), obj=dist, vtype=gp.GRB.BINARY, name="x")

    # Symmetric direction: Copy the object
    for i, j in vars.keys():
        vars[j, i] = vars[i, j]  # edge in opposite direction

    # Constraints: two edges incident to each city
    cons = m.addConstrs(vars.sum(c, "*") == 2 for c in capitals)

    m._vars = vars
    m.Params.lazyConstraints = 1
    m.Params.threads = grb_num_procs
    m.optimize(subtourelim)

    vals = m.getAttr("x", vars)
    selected = gp.tuplelist((i, j) for i, j in vals.keys() if vals[i, j] > 0.5)

    tour = subtour(selected)
    tour.remove(0)  # remove the depot

    solution = Solution.from_tour(data, tour)
    stats.collect_objective(solution.cost)
    stats.collect_runtime(perf_counter())

    return Result(solution, stats)
