#!/bin/sh
#SBATCH -J test 
#SBATCH -p cpu
#SBATCH -N 1
#SBATCH --ntasks-per-node=54
#SBATCH --time=08:00:00 
#SBATCH -A marom
 
ulimit -s unlimited
ulimit -v unlimited
# Directory for aims binary and the env 
AIMS_DIR="/home/marom_group/programs/fhi_aims_2023/aims_bin"
AIMS_BIN="$AIMS_DIR/aims.221103.scalapack.mpi.x"
AIMS_ENV="$AIMS_DIR/aims_env.sh"

source $AIMS_ENV

export OMP_NUM_THREADS=1
spack find --loaded
ldd $AIMS_BIN

mpirun -np 54 $AIMS_BIN > aims.out
