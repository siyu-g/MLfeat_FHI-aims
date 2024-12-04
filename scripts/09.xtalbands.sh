#!/bin/bash

# This script submit multiple fhi-aims calculations at once
# This calculation calculate bandstructure for crystal, GapC, VB_disp^C and CB_disp^C

rootfolder=/home/siyugao/SISSO_primary/MLfeat_FHI-aims/ # Set this to the root folder of repository
feature=bandstructure           # Specify which feature to calculate

cd $rootfolder
mkdir calculations
mkdir calculations/xtal
cd calculations 
for folder in ABECAL  ANTCEN  CENXUO  CORONE01  DBPERY  FOVVOB  HBZCOR  NAPANT01  PHNAPH  TERPHE02 # Structures to calculater
do
	mkdir xtal/$feature
	mkdir xtal/$feature/$folder
	cp $rootfolder/scripts/submit.sh xtal/$feature/$folder
	cp $rootfolder/example/testset_geometries/$folder/crystal_geometry.in xtal/$feature/$folder/geometry.in
	echo "File setup complete"
	cd xtal/$feature/$folder
	python $rootfolder/example/xtal/$feature/generate_kpath.py control geometry.in control.in   # Write the control file based on geometry	
	cat $rootfolder/example/basis.txt >> control.in
	#sbatch submit.sh
	cd $rootfolder/calculations
done


