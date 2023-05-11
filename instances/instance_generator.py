import numpy as np
import numpy.random as rnd

SEED = 42
GRID_SIZE = 100
NUM_CLIENTS = 200
NUM_INSTANCES = 100

rng = rnd.default_rng(SEED)


def manhattan_distance_matrix(coords):
    abs_diffs = np.abs(coords[:, np.newaxis, :] - coords[np.newaxis, :, :])
    dist_matrix = np.sum(abs_diffs, axis=-1)
    return dist_matrix


for idx in range(NUM_INSTANCES):
    coords = rng.integers(0, GRID_SIZE, (NUM_CLIENTS, 2), dtype=int)
    distances = manhattan_distance_matrix(coords)
    np.savetxt(
        f"instances/medium/instance_{idx}.txt", distances, delimiter=",", fmt="%d"
    )
