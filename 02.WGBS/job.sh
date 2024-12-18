#!/bin/bash
#
#SBATCH -J Remove
#SBATCH -o Log.%j.out
#SBATCH --time=UNLIMITED
#SBATCH --nodelist=node01
#SBATCH -n 6

python3 240417.RemoveXYM.py
