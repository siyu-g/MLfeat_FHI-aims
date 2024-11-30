# Ase can help get the atomic number within the crystal and its density

from ase.io import read, write

a = read("geometry.in") # Path to crystal geometry readable by ASE

print(len(a.get_masses()), sum(a.get_masses())/a.get_volume()) # This will output AtomNumC and RhoC


