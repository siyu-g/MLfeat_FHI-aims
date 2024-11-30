#!/bin/bash
#SBATCH -J relaxation# Job name
#SBATCH -n 54 # Number of total cores
#SBATCH -N 1 # Number of nodes
#SBATCH -o job_%j.out # File to which STDOUT will be written %j is the job #
#SBATCH -p cpu
#SBATCH --time=12:00:00

# Define all bins here
source /home/marom_group/SF/Siyu/SISSO/src/ENV.txt

ulimit -s unlimited
 
python calc_habs.py ABECAL.cif light 3 6
