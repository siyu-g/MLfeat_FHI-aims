#!/bin/bash

# This calculation calculate AtomNumC and RhoC for crystal
# You  can choose to calculate them one by one or use this script to create a txt file to store all the features in columns. You can specify where to store the NumAtom_Density.txt file
rootfolder=/home/siyugao/SISSO_primary/MLfeat_FHI-aims/ # Set this to the root folder of repository
feature=es           # You can go to any crystal feature folder, we just need the crystal geometry.in 

cd $rootfolder
cd calculations 
for folder in ABECAL  ANTCEN  CENXUO  CORONE01  DBPERY  FOVVOB  HBZCOR  NAPANT01  PHNAPH  TERPHE02 # Structures to calculater
do
	echo "Computing for folder $folder"
	cd xtal/$feature/$folder
        python $rootfolder/example/direct-properties/atomNumC_rhoC/get_atomNum_rho.py >> $rootfolder/calculations/NumAtom_Density.txt # Pick a path to store the file
	cd $rootfolder/calculations
done


