from pathlib import Path

import numpy as np


class ProblemData:
    def __init__(self, distances):
        self.distances = distances
        self.num_cities = len(distances)

    @classmethod
    def from_file(cls, loc):
        path = Path(loc)

        with open(path, "r") as fh:
            return cls(np.genfromtxt(fh, delimiter=","))
