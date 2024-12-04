#!/bin/bash

# This calculation calculate MolWt for single molecule
# You  can choose to calculate them one by one or use this script to create a txt file to store all the features in columns. You can specify where to store the MolWt.txt file
rootfolder=/home/siyugao/SISSO_primary/MLfeat_FHI-aims/ # Set this to the root folder of repository
feature=GapS           # You can go to any molecule feature folder, we just need the single mol geometry.in 

cd $rootfolder
cd calculations 
for folder in ABECAL  ANTCEN  CENXUO  CORONE01  DBPERY  FOVVOB  HBZCOR  NAPANT01  PHNAPH  TERPHE02 # Structures to calculater
do
	echo "Computing for folder $folder"
	cd single/$feature/$folder
        python $rootfolder/example/direct-properties/MolWtS/get_molwt.py >> $rootfolder/calculations/MolWt.txt # Pick a path to store the file
	cd $rootfolder/calculations
done


