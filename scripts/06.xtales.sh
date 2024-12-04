#!/bin/bash

# This script submit multiple fhi-aims calculations at once
# This calculation calculate Es for crystal

rootfolder=/home/siyugao/SISSO_primary/MLfeat_FHI-aims/ # Set this to the root folder of repository
feature=es           # Specify which feature to calculate

cd $rootfolder
mkdir calculations
mkdir calculations/xtal
cd calculations 
for folder in ABECAL  ANTCEN  CENXUO  CORONE01  DBPERY  FOVVOB  HBZCOR  NAPANT01  PHNAPH  TERPHE02 # Structures to calculater
do
	mkdir xtal/$feature
	mkdir xtal/$feature/$folder
	cp $rootfolder/example/xtal/$feature/control.in xtal/$feature/$folder
	cat $rootfolder/example/basis.txt >> xtal/$feature/$folder/control.in
	cp $rootfolder/scripts/submit.sh xtal/$feature/$folder
	cp $rootfolder/example/testset_geometries/$folder/crystal_geometry.in xtal/$feature/$folder/geometry.in
	echo "File setup complete"
	cd xtal/$feature/$folder
	#sbatch submit.sh
	cd $rootfolder/calculations
done


