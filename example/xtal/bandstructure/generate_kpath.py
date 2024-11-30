import numpy as np
from ase.io import read
import seekpath
import sys

'''
Input: PATH to geometry file that need to calculate the K-path (should be loadable by ASE)
Output: kpoints file / FHI-aims control.in file
Usage: 
E.g. python generate_kpath.py kpoints '/Users/siyugao12/Desktop/full_22_structs/9-PA/1-mf/1-scf/scf.in' "./kpoints_write"
E.g. python generate_kpath.py control geometry.in control.in
'''

def seek_inp(atoms):
    '''
    Generate input tensor of seekpath from ASE atoms object
    Input: Atoms object
    Output: tuple contains (cell, scaled_positions and unique atom numbers).
            See https://seekpath.readthedocs.io/en/latest/maindoc.html#aiida-integration
            for more information about the input structure
    '''
    return(atoms.cell[:], atoms.get_scaled_positions(), atoms.numbers)

def K_course(param):
    '''
    Given cell as 3 X 3 matrix, retrun the coarse k-grid as a (3, ) array
    '''
    K_course=[]
    for i in param:
        pri_vec = float(i[0]) ** 2 + float(i[1]) ** 2 + float(i[2]) ** 2
        if pri_vec < 25:
            K_course.append(8)
        elif pri_vec < 100:
            K_course.append(4)
        elif pri_vec < 400:
            K_course.append(2)
        else: K_course.append(1)
    return K_course

def generate_kpoints_file(sp_dict, outf="./kpoints"):
    '''
    Generate kpoints file from seekpath directory
    '''
    with open(outf, "w+") as myfile:
        for i, path in enumerate(sp_dict["path"]):
            if i == 0:
                myfile.write("    ".join([str("{:.10f}".format(i)) for i in sp_dict["point_coords"][path[0]]])+'  ##'+path[0]+'\n')
            elif path[0] == sp_dict["path"][i-1][1]:
                myfile.write("10"+'\n')
                myfile.write("    ".join([str("{:.10f}".format(i)) for i in sp_dict["point_coords"][path[0]]])+'  ##'+path[0]+'\n')
            else:
                myfile.write("10"+'\n')
                myfile.write("    ".join([str("{:.10f}".format(i)) for i in sp_dict["point_coords"][sp_dict["path"][i-1][1]]])+'  ##'+sp_dict["path"][i-1][1]+'\n')
                myfile.write("0"+'\n')
                myfile.write("    ".join([str("{:.10f}".format(i)) for i in sp_dict["point_coords"][path[0]]])+'  ##'+path[0]+'\n')
        myfile.write("10"+'\n')
        myfile.write("    ".join([str("{:.10f}".format(i)) for i in sp_dict["point_coords"][path[1]]])+'  ##'+path[1]+'\n')
        

def generate_control_file(sp_dict, cell,  outf="./kpoints"):
    '''
    Generate FHI-aims control.in file from seekpath directory
    '''
    with open(outf, "w+") as myfile:
        # Write control tags here:
        heading = '''# Physical settings
  xc                 pw-lda
  spin               none
  relativistic       atomic_zora scalar

# SCF settings
  sc_accuracy_rho    1E-4
  sc_accuracy_eev    1E-2
  sc_accuracy_etot   1E-5
  sc_iter_limit      40

'''	
        myfile.write(heading)
        # Write k grid based on the cell
        myfile.write("# k-point grid\n")
        myfile.write("  k_grid "+" ".join([str(i) for i in K_course(cell)])+"\n")
        # Output DOS if needed
        myfile.write('''

# output DOS
#   output dos -18.  0.  200  0.05
#   dos_kgrid_factors 4 4 4

# output band structure''')
        myfile.write('\n')
        # Start writing K path here:
        for i, path in enumerate(sp_dict["path"]):
            print(path)
            myfile.write("output band "+ " ".join([str("{:.10f}".format(i)) for i in sp_dict["point_coords"][path[0]]])+" "+ " ".join([str("{:.10f}".format(i)) for i in sp_dict["point_coords"][path[1]]])+ " 5 "+path[0]+"  "+path[1]+'\n')
        # Start writing species basis set here (currently not supported):
        ending =''''''
        myfile.write(ending) 

if __name__ == '__main__':
    write_type = sys.argv[1]  # Type of output file you want to write ("control": aims control file, "kpoints": kpoints file for QE band calculation)
    esp_inp_path = sys.argv[2]  # Input path to the geometry file, should be readable by ASE
    out_path = sys.argv[3]   # Output path
    
    # Load the atoms object from file, create the structure tuple as seekpath's input
    struct_atoms = read(esp_inp_path)
    struct = seek_inp(struct_atoms)
    cell = struct_atoms.get_cell()


    #print(seekpath.get_path(struct)['point_coords'])
    #print(seekpath.get_path_orig_cell(struct))
    if write_type == "kpoints":
    	generate_kpoints_file(seekpath.get_path_orig_cell(struct),outf=out_path)
    elif write_type == "control":
        generate_control_file(seekpath.get_path_orig_cell(struct), cell, outf=out_path)
    else:
        print("Write type not found")
