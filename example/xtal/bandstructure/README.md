This folder contains example python script to write input for band sctrucure calculation. 
Through the calculation you can get three primary features, 
* Gap^C: The crystal band gap value
* VBdisp^C: The valence band dispersion, calculated by the energy range of the top valence band
* CBdisp^C: The conduction band dispersion, calculated by the energy range of the bottom conduction band

The folder contains scripts to generate the k-path in control.in file according to different Bravais lattice type.
Before the calculation, run generate_kpath.py:
 python generate_kpath.py control $PATH_TO_Crystal_geometry.in ./control.in
generate_kpath.py will also write the corresponding k_grid based on the cell length. This k_grid settings can be applied to all other crystal features.
An example control.in is shown in the folder


After the calculation, the three features listed above can be gathered by running the get_dispersion.py:
 python get_dispersion.py


