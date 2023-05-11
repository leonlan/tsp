from copy import copy
from typing import Optional, List

from tsp.classes.ProblemData import ProblemData


class Solution:
    def __init__(
        self,
        tour: list[int],
        unassigned: Optional[list[int]] = None,
        cost: Optional[int] = None,
    ):
        self.tour = tour
        self.unassigned = unassigned or []
        self.cost = cost or None

    def __deepcopy__(self, memo={}):
        return Solution(copy(self.tour), copy(self.unassigned), copy(self.cost))

    def __repr__(self):
        return str(self.tour)

    def __len__(self):
        return len(self.tour)

    def __eq__(self, other):
        return self.tour == other.tour

    @staticmethod
    def compute_distance(data, tour):
        """
        Computes the total travel distance of the tour.
        """
        visits = [0] + tour + [0]
        return data.distances[visits[1:], visits[:-1]].sum()

    def objective(self):
        """
        Alias for cost, because ALNS requires the ``objective()`` method.
        """
        return self.cost

    def opt_insert(self, data: ProblemData, customer: int):
        """
        Optimally inserts the customer in the current tour.
        """
        idcs_costs = []

        for idx in range(len(self.tour) + 1):
            cost = self._insert_cost(data, idx, customer)
            idcs_costs.append((idx, cost))

        idx, _ = min(idcs_costs, key=lambda idx_cost: idx_cost[1])
        self.insert(idx, customer)

    def _insert_cost(self, data: ProblemData, idx: int, cust: int) -> int:
        if len(self.tour) == 0:
            pred, succ = 0, 0
        elif idx == 0:
            pred, succ = 0, self.tour[idx]
        elif idx == len(self.tour):
            pred, succ = self.tour[idx - 1], 0
        else:
            pred, succ = self.tour[idx - 1], self.tour[idx]

        delta = data.distances[pred, cust] + data.distances[cust, succ]
        delta -= data.distances[pred, succ]

        return delta

    def insert(self, idx: int, customer: int):
        """
        Inserts the customer at position idx.
        """
        self.tour.insert(idx, customer)

    def remove(self, customer: int):
        """
        Removes the customer from the tour.
        """
        self.tour.remove(customer)

    def update_cost(self, data: ProblemData):
        # The update_cost method is needed to set a cost for a complete
        # solution that ALNS can access with the `objective()` method.
        self.cost = self.compute_distance(data, self.tour)

    @classmethod
    def from_tour(self, data: ProblemData, tour: List[int]):
        """
        Creates a Solution object from a tour.
        """
        cost = self.compute_distance(data, tour)
        return Solution(tour, cost=cost)
