# Yiqun Luo (luo2@andrew.cmu.edu)
# 
# This script is used to extract features from the AIMS output files.
# To be updated constantly.

import argparse
import os
import json
from ase.io import read
import re
try:
    from ccdc import io
except:
    print("CCDC is not installed.")


def total_energy(path : str) -> float:
    assert os.path.exists(path), path + " not exist!"
    with open(path) as f:
        once = False
        cal_success = False
        for line in f:
            if "| Total energy of the DFT / Hartree-Fock s.c.f. calculation      :" in line:
                assert not once, "Two 'Total energy of the DFT / Hartree-Fock s.c.f. calculation' in " + path
                E = float(re.findall("[\-\+\d\.]+", line)[-1])
                once = True
            if "Have a nice day." in line:
                assert not cal_success, "Double 'Have a nice day.'"
                cal_success = True
        if not cal_success:
            print("DFT calculation fails:" + path)
            return None
        assert E, "No 'Total energy of the DFT / Hartree-Fock s.c.f. calculation' found in " + path
        return E


def gap_s(struct : str) -> None:
    path = os.path.join("single/es", struct, "aims.out")
    if os.path.exists(path):
        gap = None
        with open(path) as f:
            for line in f:
                if "Overall HOMO-LUMO gap:" in line:
                    gap = re.findall("[\+\-\d\.]+", line)[-2]
        if gap:
            feature[struct]["gap_s"] = float(gap)
            print(f"gap_s for {struct}: {feature[struct]['gap_s']}")
        else:
            print("DFT calculation fails:" + path)
    return

def Et_s(struct : str) -> None:
    path_ground = os.path.join("single/es", struct, "aims.out")
    path_Et = os.path.join("single/et", struct, "aims.out")
    if os.path.exists(path_ground) and os.path.exists(path_Et):
        Et = total_energy(path_Et)
        E0 = total_energy(path_ground)
        if Et and E0:
            feature[struct]["Et_s"] = Et - E0
            print(f"Et_s for {struct}: {feature[struct]['Et_s']}")
    return

def DF_s(struct : str) -> None:
    if "gap_s" in feature[struct] and "Et_s" in feature[struct]:
        feature[struct]["DF_s"] = float(feature[struct]["gap_s"]) - 2 * float(feature[struct]["Et_s"])
        print(f"DF_s for {struct}: {feature[struct]['DF_s']}")
    return

def EA_s(struct : str) -> None:
    path_N = os.path.join("single/es", struct, "aims.out")
    path_Np1 = os.path.join("single/ea", struct, "aims.out")
    if os.path.exists(path_N) and os.path.exists(path_Np1):
        EN = total_energy(path_N)
        ENp1 = total_energy(path_Np1)
        if EN and ENp1:
            feature[struct]["EA_s"] = EN - ENp1
            print(f"EA_s for {struct}: {feature[struct]['EA_s']}")
    return

def weight_s(struct : str) -> None:
    path = os.path.join("single/es", struct, "geometry.in")
    if os.path.exists(path):
        try:
            feature[struct]["weight_s"] = sum(read(path, format = "aims").get_masses())
            print(f"weight_s for {struct}: {feature[struct]['weight_s']}")
        except:
            print("geometry.in wrong format:" + path)
    return
"""
def density(struct : str) -> None:
    path = os.path.join("1-125eV", struct, "crystal_geometry.in")
    if os.path.exists(path):
        cell = read(path, format = "aims")
        feature[struct]["density"] = sum(cell.get_masses()) / cell.get_volume()
        print(f"Density for {struct}: {feature[struct]['density']}")
    return
"""
def density(struct : str) -> None:
    if "io" in globals():
        crystal_reader = io.CrystalReader("CSD")
        e = crystal_reader.crystal(struct)
        with io.CrystalWriter('some_refcodes.cif', append=True) as crystal_writer:
            crystal_writer.write(e)
        cell = read('some_refcodes.cif')
        feature[struct]["density"] = sum(cell.get_masses()) / cell.get_volume()
        print(f"Density for {struct}: {feature[struct]['density']}")
        os.remove('some_refcodes.cif')
    return

def write(struct : str) -> None:
    if args.overwrite or struct not in feature:
        feature[struct] = {}
        gap_s(struct)
        Et_s(struct)
        DF_s(struct)
        EA_s(struct)
        weight_s(struct)
        density(struct)
    else:
        if (not "gap_s" in feature[struct]) or (not feature[struct]["gap_s"]):
            gap_s(struct)
        if (not "Et_s" in feature[struct]) or (not feature[struct]["Et_s"]):
            Et_s(struct)
        if (not "DF_s" in feature[struct]) or (not feature[struct]["DF_s"]):
            DF_s(struct)
        if (not "EA_s" in feature[struct]) or (not feature[struct]["EA_s"]):
            EA_s(struct)
        if (not "weight_s" in feature[struct]) or (not feature[struct]["weight_s"]):
            weight_s(struct)
        if (not "density" in feature[struct]) or (not feature[struct]["density"]):
            density(struct)
    print("\n")
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", default = "stats.json", help = "Path to the existing JSON file")
    parser.add_argument("--outfile", default = "stats.json", help = "Path to the output JSON file")
    parser.add_argument("--overwrite", action = "store_true", default = False, help = "Whether or not to overwrite an existing property.")
    parser.add_argument("structs", nargs = '+', help = "List of structures to be collected")
    args = parser.parse_args()

    feature = {}
    if os.path.exists(args.infile) and (not args.overwrite):
        with open(args.infile) as f:
            feature = json.load(f)

    for struct in args.structs:
        write(struct)

    with open(args.outfile, 'w') as f:
        json.dump(feature, f, indent = 4)
