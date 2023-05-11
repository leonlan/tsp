from genericpath import exists
from pathlib import Path
import argparse
from subprocess import check_call


def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(prog="batch")

    parser.add_argument("instances", nargs="+", help="Instance paths.")

    parser.add_argument("--chunk_size", type=int)

    parser.add_argument("--out_dir", type=str)
    parser.add_argument("--config_loc", type=str)

    return parser.parse_args()


def main():
    args = dict(**vars(parse_args()))

    instances = args["instances"]
    n_instances = len(instances)

    chunk_size = args["chunk_size"]

    # Make the out directory
    Path(args["out_dir"]).mkdir(parents=True, exist_ok=True)

    for idx in range(n_instances // chunk_size + 1):
        instances_chunk = instances[idx * chunk_size : (idx + 1) * chunk_size]

        # Run sbatch with time limit on ``chunk_size`` instances.
        call = (
            ["sbatch"]
            + ["bmsX"]
            + [args["out_dir"]]
            + [args["config_loc"]]
            + [str(idx)]
            + instances_chunk
        )
        check_call(call)


# mkdir 230227-cvrp
# python batcherX.py instances/X/*.vrp --chunk_size 16 --out_dir 230227-cvrp --config_loc configs/cvrp.toml

if __name__ == "__main__":
    main()
