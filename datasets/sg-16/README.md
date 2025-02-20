Siyu's testset for 16 structures in SISSOonPAH101 paper

1. create.py: python code to parse all the data from a formatted excel file to CSV, and load the CSV to prepare input for SISSO predictions.
Input: xlsx file; Output: CSV file; predict-test-*.dat

2. CSV file: features and target stored in CSV format. Normally input for all subsequent analysis.
   

3. predit-test-*.dat: ready-to-use file for SISSO prediction. All the target values are simulated by BerkeleyGW software. Simulation details are same as PAH101 dataset, and could be found in the paper: https://chemrxiv.org/engage/chemrxiv/article-details/6751cee35a82cea2fa182d3d

   es: singlet excitation energy; et: triplet excitation energy; est: singlet-triplet gap; sbd: singlet excitation binding energy. Details for these properties and example to use them could be found in paper: https://chemrxiv.org/engage/chemrxiv/article-details/6761cf87fa469535b9ec1c84

