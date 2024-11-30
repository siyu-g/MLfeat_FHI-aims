from ase.io import read, write

a = read("geometry.in") # Path to single molecule geometry
print(a.get_masses())
