import numpy as np
import os

def get_fermi(file_name):
    '''Get list of energies of Fermi and Fermi +1 bands'''
    # Load data from file
    data = np.loadtxt(open(file_name))
    occup_env = data[:,4:]
    
    # Extract the data to array of occupancy and energy, occupancy is the odd columns, energy is the even columns
    occupancy = occup_env[ :, ::2]
    energy = occup_env[:, 1::2]
    #print(np.shape(occupancy))

    # Find the index of HOMO, which is the first index whose occupancy turn from 2.0 to 0.0
    homo_idx = np.where(occupancy[0] == 0)[0][0] - 1    
    #print("HOMO band index:", homo_idx)

    # Get Fermi band and Fermi +1 band, which are the two bands we care about
    Fermi = energy[:, homo_idx]
    Fermi_p1 = energy[:, homo_idx +1]
    return Fermi, Fermi_p1 



if __name__ == "__main__":
    # Get list of band files for different high symmetry k points
    file_list = [filename for filename in os.listdir('.') if filename.startswith("band1")]
 
    # Get the full Fermi and Fermi+1 band by concatenating different k points
    fermi = []
    fermi_p1 = []
    for file_name in file_list:
        fermi_k, fermip1_k = get_fermi(file_name)
        fermi.append(fermi_k)
        fermi_p1.append(fermip1_k)
    VB = np.array(fermi).reshape(-1, 1)
    CB = np.array(fermi_p1).reshape(-1, 1)
    
    # Get the VB and CB dispersion
    VB_disp = (max(VB) - min(VB))[0]
    CB_disp = (max(CB) - min(CB))[0]
    
    # Get Band Gap
    band_gap = (min(CB) - max(VB))[0]
    
    print(VB_disp, CB_disp, band_gap)

