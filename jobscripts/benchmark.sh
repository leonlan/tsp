#!/usr/bin/env bash

#SBATCH --job-name=benchmark
#SBATCH --time 1:00:00
#SBATCH --nodes 1
#SBATCH --partition=normal
#SBATCH --constraint=gold_6130
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=l.lan@vu.nl
#SBATCH --out=slurm/%A_%a.out

poetry run python benchmark.py instances/medium/* --algorithm alns --max_iterations 1000
