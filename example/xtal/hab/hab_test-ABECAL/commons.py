#These paths to executables are used by the calculation scripts in the scripts folder of this package.
#Please adjust them according to your needs.

aims_binary = '/home/marom_group/programs/fhi_aims_2023/aims_bin/aims.221103.scalapack.mpi.x > aims.out'
#aims_binary='/data/kick/programs/aims/bin/aims.160714.mpi.x'
#aims_binary="/data/heenen/TOOLS/AIMS/bin/aims.161219.scalapack.mpi.x < /dev/null | tee aims.out"
aims_species = '/home/marom_group/programs/fhi_aims_2023/fhi-aims.221103/species_defaults/defaults_2010/'
#mpiexe = 'mpirun'
mpiexe = 'mpirun'
lammps_binary = 'mpirun -np 8 /home/xingyu/software/lammps-11Aug17/src/lmp_mpi < in_lammps'
