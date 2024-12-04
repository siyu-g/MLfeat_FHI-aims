from ase.io import read, write

a = read("geometry.in") # Path to single molecule geometry
print(sum(a.get_masses()))
