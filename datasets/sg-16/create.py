import pandas as pd
import numpy as np
import glob
import json
import os

np.random.seed(0)
def prep_data(file_name):
    '''Preposessing and get the updated Dataframe'''
    # Load data from xlsx file
    FILEPATH = "SISSO_new_testset.xlsx"
    data_df = pd.read_excel(FILEPATH, sheet_name="All_features", nrows=18).sort_values(by=["CSD Reference Code"])
    # Data cleaning: Non-predictable rows
    incompleted_data = ["ICAPOR01(OH1)", "TETCEN-T1"]
    data_df = data_df[~data_df["CSD Reference Code"].isin(incompleted_data)].sort_values(by=["CSD Reference Code"])


    # Calculate the singlet and triplet binding energy
    data_df["Singlet_binding"] =  data_df["GW_QP_BandGap"] - data_df["GWBSE_EsC"]
    data_df["Triplet_binding"] =  data_df["GW_QP_BandGap"] - data_df["GWBSE_EtC"]
    

    # Save the new Dataframe to a file
    data_df.to_csv(file_name, sep="\t", header = True, index_label="csv_idx")
    print("Data prep finished, CSV file is ready")

def create_dat(data, feature_list, property, outpath):
    '''This function creates SISSO input train.dat/valid.dat.
    Input Description:
    data: Dataframe which contains all info
    feature_list: 1D list of feature. Type: list
    property: regression property. Type: str
    outpath: path to store the dat file
    Output: None
    '''
    df_out = data.rename(columns={"CSD Reference Code": "materials", property: "property"})

    # Change the initial column names to materials, property, feature1, feature2, ...
    columns = ["materials", "property"]
    # for n, feature in enumerate(feature_list):
    #     df_out = df_out.rename(columns={feature: "feature%s" % n})
    #     columns.append("feature%s" % n)
    # for column in columns:
    #     df_out[column] = df_out[column].astype("float64")

    columns = ["materials", "property"] + feature_list
    
    # Output the dataframe to file
    df_out[columns].to_csv(outpath, sep=" ", header = True, index=False)

if __name__=="__main__":
    # file_name of csv file
    file_name = "SISSO_testset_calculation_info_03012025.csv"
    # Prepossesing the data and save it to CSV file, if already have CSV file, comment out the following line
    prep_data(file_name)

    # Load Dataframe from CSV file
    data_df = pd.read_csv(file_name, sep="\t")

    # Add two columns representing DFT Singlet-Triplet transition driving force
    data_df["DFC_ST"] = data_df["GapC"] - data_df["ETC"]
    data_df["DFS_ST"] = data_df["GapS"] - data_df["ETS"]   

    # # Initial test set reference code
    # test_ref = ["NAPANT01", "PHNAPH", "ABECAL","ANTCEN", "DBPERY", "CENXUO", "HBZCOR", "CORONE01", "TERPHE02", "FOVVOB"]
    
    # # Get test Dataframe and train/valid Dataframe by CSD Reference Code
    # test_df = data_df[data_df["CSD Reference Code"].isin(test_ref)]
    # train_valid_df = data_df[~data_df["CSD Reference Code"].isin(test_ref)]


    # Feature list for Case 1, 14 columns, to predict BSE Singlet exciton energy
    feature_list_es = ['GapC', 'ETC', 'VBdispC', 'CBdispC', 'Hab', 'GapS', 'ETS', 
                       'IPS', 'EAS', 'PolarTensorS', 'AtomNumC', 'RhoC', 'EpsilonC', 'MolWtS'
                       ]
    # Feature list for Case 2, 14 columns, to predict BSE Triplet exciton energy
    feature_list_et = ['GapC', 'ETC', 'VBdispC', 'CBdispC', 'Hab', 'GapS', 'ETS', 
                       'IPS', 'EAS', 'PolarTensorS', 'AtomNumC', 'RhoC', 'EpsilonC', 'MolWtS'
                       ]

    # Feature list for Case 3, 16 columns, to predict BSE Singlet-Triplet gap
    feature_list_est = ['GapC', 'ETC', 'VBdispC', 'CBdispC', 'Hab', 'GapS', 'ETS', 
                        'IPS', 'EAS', 'DFC_ST', 'DFS_ST', 'PolarTensorS', 'AtomNumC', 'RhoC', 'EpsilonC', 'MolWtS'                       
                        ]

    # Feature list for Case 4, 16 columns, to predict BSE Singlet Fission driving force
    feature_list_df = ['GapC', 'ETC', 'VBdispC', 'CBdispC', 'Hab', 'GapS', 'ETS', 
                        'IPS', 'EAS', 'DFC', 'DFS', 'PolarTensorS', 'AtomNumC', 'RhoC', 'EpsilonC', 'MolWtS'                       
                        ]

    # Feature list for Case 5, 14 columns, to predict BSE Binding energy
    feature_list_binding = ['GapC', 'ETC', 'VBdispC', 'CBdispC','Hab', 'GapS', 'ETS',
                       'IPS', 'EAS', 'PolarTensorS', 'AtomNumC', 'RhoC', 'EpsilonC', 'MolWtS'
                       ]

    # # Create random indicies to leave-10-out from training data
    # ntime = 40
    # for i in range(ntime):

    #     valid_df = train_valid_df.sample(n = 10) # Randomly sample 10 rows from initial data as valid data
    #     train_df = train_valid_df.drop(valid_df.index)  # The leftover are training data
    #     try:
    #         os.mkdir("cross_validate%s" % i)
    #     except FileExistsError:
    #         pass

    #     # Create dat file from dataframe based on actual case
    #     '''
    #     # Case 1. SISSO training for optical gap Es
    #     # Description: Es is the target value, use selected 14 DFT features (exclude "DFS" and "DFC") from dataframe
    #     print(train_df.keys())
        
    #     create_dat(data= valid_df, feature_list=feature_list_es, property="GWBSE_EsC", outpath="cross_validate%s/validation.dat" % i)
    #     create_dat(data= train_df, feature_list=feature_list_es, property="GWBSE_EsC", outpath="cross_validate%s/train.dat" % i)

    #     '''

    #     # Case 2. SISSO training for triplet excitation energy Et
    #     # Description: Et is the target value, use selected 14 DFT features (exclude "DFS" and "DFC") from dataframe
    #     print(train_df.keys())
        
    #     create_dat(data= valid_df, feature_list=feature_list_et, property="GWBSE_EtC", outpath="cross_validate%s/validation.dat" % i)
    #     create_dat(data= train_df, feature_list=feature_list_et, property="GWBSE_EtC", outpath="cross_validate%s/train.dat" % i)
        
    #     # Case 3. SISSO training for S-T exciton gap 
    #     # Description: GWBSE_DeltaEstC is the target value, use DeltaEst of DFT for single molecule and crystal to replace
    #     #              "DFC" and "DFS"
     
    #     # create_dat(data= valid_df, feature_list=feature_list_est, property="GWBSE_DeltaEstC", outpath="cross_validate%s/validation.dat" % i)
    #     # create_dat(data= train_df, feature_list=feature_list_est, property="GWBSE_DeltaEstC", outpath="cross_validate%s/train.dat" % i)

    #     # Case 4. SISSO training for SF driving force (Initial training in matml_workflow) 
    #     # Description: SF driving force is the target value
     
    #     # create_dat(data= valid_df, feature_list=feature_list_df, property="SF Driving Force", outpath="cross_validate%s/validation.dat" % i)
    #     # create_dat(data= train_df, feature_list=feature_list_df, property="SF Driving Force", outpath="cross_validate%s/train.dat" % i)
        
    # Create dat file for prediction purpose
    create_dat(data= data_df, feature_list=feature_list_es, property="GWBSE_EsC", outpath="predict-test-es.dat")
    create_dat(data= data_df, feature_list=feature_list_et, property="GWBSE_EtC", outpath="predict-test-et.dat")
    create_dat(data= data_df, feature_list=feature_list_est, property="GWBSE_DeltaEstC", outpath="predict-test-est.dat")
    create_dat(data= data_df, feature_list=feature_list_binding, property="Singlet_binding", outpath="predict-test-sbd.dat")
