#!/usr/bin/env python
import sys
import os
import shutil

from aimsutils import aims_calc_params
import json
from aimsutils.fodft.aims import FoAims
from orgel_base.search.dimers import find_unique_dimers_cif
from orgel_base.cluster.density_based import density_based_clustering
from commons import aims_binary, aims_species, mpiexe
from orgel_base.search.hashing import do_hashing, get_moment_com_dist

#Remove again
from aimsutils.fodft import get_molecule_hash

########################
## Note to the users:
## Please adjust the paths to the executables and helper files in
## commons.py before running this script.
########################
########################
## Example for running this script:
## python calc_habs.py ../examples/DAZCOE.cif tight 3 6
########################


def prepare_aims(binary_in, specpath_in, ncpu_in, xc_in="blyp",
                 species_in="light"):
    """
    Prepare the aims_params dict for the ASE aims calculator.
    """
    aims_params = aims_calc_params(binary_path=binary_in,
                                   species_path=specpath_in,
                                   xc=xc_in,
                                   species=species_in,
                                   mpiexe=mpiexe,
                                   numcpu=ncpu_in,
				   default="organic_fodft")
    aims_params["relativistic"] = "zora scalar 1e-12"
    aims_params["packed_matrix_format"] = "index"
    return aims_params

if __name__ == '__main__':
    try:
    	cif = str(sys.argv[1])
    except:
        cif="../examples/QEKYAG.cif"
    try:
        species_default=str(sys.argv[2])
    except:
        species_default="light" #"light.ext"
    try:
        mult = int(sys.argv[3]) #multiplicator for input cell
    except:
        mult=4
    try:
        cutoff = float(sys.argv[4])
    except:
        cutoff=3

    print("Settings for calculation:")
    print("-------------------------")  
    print("Cif: {0}".format(cif))
    print("Species_default: {0}".format(species_default))
    print("Multiplicator: {0}".format(mult))
    print("Cutoff: {0}".format(cutoff))
    print("Aims species: {0}".format(aims_species))
    print("Aims binary: {0}".format(aims_binary))
    print("-------------------------")

    # prepare aims parameters for the ASE calculator
    aims_params = prepare_aims(aims_binary, aims_species,
                               species_in=species_default, ncpu_in=56)

    # cifs = glob.glob('*.cif')
    cifs = [cif]
    cwd = os.getcwd()

    print(len(density_based_clustering(cif, multiplicator=4, square_mult=True, cleanup=True)[0].get_chemical_symbols()))

    for cif in cifs:
        name, data, unique = find_unique_dimers_cif(cif,mult,cutoff)
        try:
            os.mkdir(name)
            os.chdir(name)

            fo_calcs = []
            for d in unique:
                #f1, f2 = density_based_clustering(d[1], mult, square_mult=True,
                #                                  cleanup=True,
                #                                  target_num_molecules=2)
		
                f1,f2=d[1][0],d[1][1]
                dimer=f1+f2
                hashed=do_hashing(get_moment_com_dist, [dimer,f2,f1], orientation_dependent=True, charge_dependent=True)
                fo_calcs.append([FoAims(fragment1=f1, fragment2=f2,
                                        charges=[+1, 0], fo_type='hole',
                                        **aims_params), d[0]])
#		import numpy as np	
#		print (np.linalg.norm(f1.get_center_of_mass()-f2.get_center_of_mass()))
	        
            # do the calculations and retrieve H_ab

            calc_data = {}
            for calc in fo_calcs:
                ident, habs, states = calc[0].do_calculations()
                calc_data[calc[1]] = [habs, states, ident]

            with open('hab_dump.json', 'w') as f:
                json.dump(calc_data, f)

            # prepare all data necessary for graph (all but Atoms-obj)
            ddump = [data.coms, [x.tolist() for x in data.moments], data.hashs,
                     data.edges]
            with open('data_dump.json', 'w') as f:
                json.dump(ddump, f)
            # with open('uni_dump.pickle', 'wb') as f:
                # pickle.dump(unique, f)

        finally:
            os.chdir(cwd)
	

        name2=name+'_2'
        try:
            os.mkdir(name2)
            os.chdir(name2)
	    
            fo_calcs = []
            for d in unique:
                #f1, f2 = density_based_clustering(d[1], mult, square_mult=True,
                #                                  cleanup=True,
                #                                  target_num_molecules=2)

                f1,f2=d[1][1],d[1][0]
                dimer=f1+f2
                hashed=do_hashing(get_moment_com_dist, [dimer,f1,f2], orientation_dependent=True, charge_dependent=True)
                fo_calcs.append([FoAims(fragment1=f1, fragment2=f2,
                                        charges=[+1, 0], fo_type='hole',
                                        **aims_params), d[0]])

            # do the calculations and retrieve H_ab

            calc_data = {}
            for calc in fo_calcs:
                ident, habs, states = calc[0].do_calculations()
                calc_data[calc[1]] = [habs, states, ident]

            with open('hab_dump.json', 'w') as f:
                json.dump(calc_data, f)

            # prepare all data necessary for graph (all but Atoms-obj)
            ddump = [data.coms, [x.tolist() for x in data.moments], data.hashs,
                     data.edges]
            with open('data_dump.json', 'w') as f:
                json.dump(ddump, f)
            # with open('uni_dump.pickle', 'wb') as f:
                # pickle.dump(unique, f)

        finally:
            os.chdir(cwd)
	
