#!/bin/bash

# This script submit multiple fhi-aims calculations at once
# This calculation calculate IPS

rootfolder=/home/siyugao/SISSO_primary/MLfeat_FHI-aims/ # Set this to the root folder of repository
feature=ip           # Specify which feature to calculate

cd $rootfolder
mkdir calculations
mkdir calculations/single
cd calculations 
for folder in ABECAL  ANTCEN  CENXUO  CORONE01  DBPERY  FOVVOB  HBZCOR  NAPANT01  PHNAPH  TERPHE02 # Structures to calculater
do
	mkdir single/$feature
	mkdir single/$feature/$folder
	cp $rootfolder/example/single/$feature/control.in single/$feature/$folder
	cat $rootfolder/example/basis.txt >> single/$feature/$folder/control.in
	cp $rootfolder/scripts/submit.sh single/$feature/$folder
	cp $rootfolder/example/testset_geometries/$folder/singlemol_geometry.in single/$feature/$folder/geometry.in
	echo "File setup complete"
	cd single/$feature/$folder
#	sbatch submit.sh
	cd $rootfolder/calculations
done


