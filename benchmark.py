import argparse

from functools import partial
from pathlib import Path
from typing import List, Optional

import numpy as np
from tqdm.contrib.concurrent import process_map

from tsp import solve_alns, solve_lkh, solve_milp
from tsp.classes import ProblemData


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("instances", nargs="+", help="Instance paths.")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--num_procs", type=int, default=8)
    parser.add_argument("--pct_destroy", type=float, default=0.2)
    parser.add_argument(
        "--algorithm", type=str, default="alns", choices=["alns", "lkh", "milp"]
    )
    parser.add_argument("--sol_dir", type=str)
    parser.add_argument("--grb_num_procs", type=int, default=1)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--max_runtime", type=float)
    group.add_argument("--max_iterations", type=int)

    return parser.parse_args()


def maybe_mkdir(where: str):
    if where:
        directory = Path(where)
        directory.mkdir(parents=True, exist_ok=True)


def tabulate(headers, rows) -> str:
    # These lengths are used to space each column properly.
    lengths = [len(header) for header in headers]

    for row in rows:
        for idx, cell in enumerate(row):
            lengths[idx] = max(lengths[idx], len(str(cell)))

    header = [
        "  ".join(f"{h:<{l}s}" for l, h in zip(lengths, headers)),
        "  ".join("-" * l for l in lengths),
    ]

    content = [
        "  ".join(f"{str(c):>{l}s}" for l, c in zip(lengths, row)) for row in rows
    ]

    return "\n".join(header + content)


def solve(
    loc: str,
    seed: int,
    algorithm: str,
    sol_dir: Optional[str],
    **kwargs,
):
    """
    Solves a single instance, and returns a tuple with the results. Any
    additional keyword arguments are passed to ``solve()``.

    Parameters
    ----------
    loc
        Path to the instance to solve.
    seed
        Random seed.
    algorithm
        Algorithm to use.
    sol_dir
        Directory to save the solution to.
    **kwargs
        Optional keyword arguments to pass to ``solve()``.

    Returns
    -------
    Solver results.
    """
    path = Path(loc)
    data = ProblemData.from_file(loc)

    if algorithm == "alns":
        res = solve_alns(seed, data=data, **kwargs)
    elif algorithm == "lkh":
        res = solve_lkh(seed, data=data, **kwargs)
    elif algorithm == "milp":
        res = solve_milp(seed, data=data, **kwargs)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    best = res.best_state

    if sol_dir:
        instance_name = Path(loc).stem
        where = Path(sol_dir) / (f"{instance_name}-{algorithm}" + ".sol")

        with open(where, "w") as fh:
            fh.write(str(res.best_state))

    return (
        path.stem,
        best.cost,
        len(res.statistics.objectives),
        round(res.statistics.total_runtime, 3),
        algorithm,
    )


def benchmark(instances: List[str], **kwargs):
    """
    Solves a list of instances, and prints a table with the results. Any
    additional keyword arguments are passed to ``solve()``.

    Parameters
    ----------
    instances
        Paths to the instances to solve.
    """
    maybe_mkdir(kwargs.get("sol_dir", ""))
    maybe_mkdir(kwargs.get("plot_dir", ""))

    if len(instances) == 1:
        res = solve(instances[0], **kwargs)
        print(res)
        return

    func = partial(solve, **kwargs)
    func_args = sorted(instances)

    tqdm_kwargs = {"max_workers": kwargs.get("num_procs", 1), "unit": "instance"}
    data = process_map(func, func_args, **tqdm_kwargs)

    dtypes = [
        ("inst", "U37"),
        ("obj", int),
        ("iters", int),
        ("time", float),
        ("alg", "U37"),
    ]

    data = np.asarray(data, dtype=dtypes)
    headers = ["Instance", "Obj.", "Iters. (#)", "Time (s)", "Algorithm"]

    print("\n", tabulate(headers, data), "\n", sep="")
    print(f"      Avg. objective: {data['obj'].mean():.0f}")
    print(f"     Avg. iterations: {data['iters'].mean():.0f}")
    print(f"   Avg. run-time (s): {data['time'].mean():.2f}")


def main():
    benchmark(**vars(parse_args()))


if __name__ == "__main__":
    main()
