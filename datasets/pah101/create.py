import pandas as pd
import numpy as np
import glob
import json
import os

np.random.seed(0)
def prep_data():
    '''Preposessing and get the updated Dataframe'''
    # Load data from xlsx file
    FILEPATH = "41524_2022_758_MOESM2_ESM.xlsx"
    data_df = pd.read_excel(FILEPATH, nrows=101).sort_values(by=["CSD Reference Code"])
    df_eps = pd.read_excel("../Plots_pah101/pah101_gw_epsilon.xlsx")
    df_eps = df_eps.rename(columns={"CSD_Reference": "CSD Reference Code", "gw_epsilon": "GW_EpsilonC", "QP_VBM(eV)": "GW_QP_VBM", "QP_CBM(eV)": "GW_QP_CBM"})
    print(df_eps)
    # loop through json data and get the Et and Es values, calculate Es Et gaps
    systems = glob.glob("../data/*.json")
    Es = {}
    Et = {}
    Es_t = {}
    for sys_path in np.sort(systems):
        data = json.load(open(sys_path))
        name = data['struct_id']
        # Add columns to data frame, map between refcode and Et, Es-Et values
        Es[data["gwbse"]["bse_Es"]]= name
        Et[data["gwbse"]["bse_Et"]]= name
        Es_t[data["gwbse"]["bse_Es"]-data["gwbse"]["bse_Et"]] = name

    # Add GW Es and Et, CBM, VBM to columns
    data_df["GWBSE_EsC"] = Es
    data_df["GWBSE_EtC"] = Et
    data_df["GWBSE_DeltaEstC"] = Es_t
    
    # Merge the Collected GW results from epsilon xlsx to the dataframe
    data_df = pd.merge(data_df, df_eps, on='CSD Reference Code')
    data_df["GW_QP_BandGap"] = data_df["GW_QP_CBM"] - data_df["GW_QP_VBM"]
    data_df["Singlet_binding"] =  data_df["GW_QP_BandGap"] - data_df["GWBSE_EsC"]
    data_df["Triplet_binding"] =  data_df["GW_QP_BandGap"] - data_df["GWBSE_EtC"]
    
    # Save the new Dataframe to a file
    data_df.to_csv("PAH101_calculation_info_04162024.csv", sep="\t", header = True, index_label="csv_idx")
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
    # Prepossesing the data and save it to CSV file, if already have CSV file, comment out the following line
    # prep_data()

    # Load Dataframe from CSV file
    data_df = pd.read_csv("PAH101_calculation_info_04162024.csv", sep="\t")
    
    # Initial test set reference code
    test_ref = ["NAPANT01", "PHNAPH", "ABECAL","ANTCEN", "DBPERY", "CENXUO", "HBZCOR", "CORONE01", "TERPHE02", "FOVVOB"]
    
    # Get test Dataframe and train/valid Dataframe by CSD Reference Code
    test_df = data_df[data_df["CSD Reference Code"].isin(test_ref)]
    train_valid_df = data_df[~data_df["CSD Reference Code"].isin(test_ref)]

    # Create random indicies to leave-10-out from training data
    ntime = 40
    for i in range(ntime):

        valid_df = train_valid_df.sample(n = 10) # Randomly sample 10 rows from initial data as valid data
        train_df = train_valid_df.drop(valid_df.index)  # The leftover are training data
        os.mkdir("cross_validate%s" % i)

        # Create dat file from dataframe based on actual case

        # Case 1. SISSO training for optical gap Es
        # Description: Es is the target value, use selected 14 DFT features (exclude "DFS" and "DFC") from dataframe
        print(train_df.keys())
        feature_list_es = ['GapC', 'ETC', 'VBdispC', 'CBdispC', 'Hab', 'GapS', 'ETS', 
                       'IPS', 'EAS', 'PolarTensorS', 'AtomNumC', 'RhoC', 'EpsilonC', 'MolWtS'
                       ]
        
        create_dat(data= valid_df, feature_list=feature_list_es, property="GWBSE_EsC", outpath="cross_validate%s/validation.dat" % i)
        create_dat(data= train_df, feature_list=feature_list_es, property="GWBSE_EsC", outpath="cross_validate%s/train.dat" % i)

        '''
        # Case 2. SISSO training for S-T exciton gap 
        # Description: GWBSE_DeltaEstC is the target value, use DeltaEst of DFT for single molecule and crystal to replace
        #              "DFC" and "DFS"

        # First create the two new features from previous DFT features
        valid_df["DFC_ST"] = valid_df["GapC"] - valid_df["ETC"]
        valid_df["DFS_ST"] = valid_df["GapS"] - valid_df["ETS"]
        train_df["DFC_ST"] = train_df["GapC"] - train_df["ETC"]
        train_df["DFS_ST"] = train_df["GapS"] - train_df["ETS"]

        feature_list_est = ['GapC', 'ETC', 'VBdispC', 'CBdispC', 'Hab', 'GapS', 'ETS', 
                        'IPS', 'EAS', 'PolarTensorS', 'AtomNumC', 'RhoC', 'EpsilonC', 'MolWtS',
                        'DFC_ST', 'DFS_ST'
                        ]
        
        create_dat(data= valid_df, feature_list=feature_list_est, property="GWBSE_DeltaEstC", outpath="cross_validate%s/validation.dat" % i)
        create_dat(data= train_df, feature_list=feature_list_est, property="GWBSE_DeltaEstC", outpath="cross_validate%s/train.dat" % i)
        '''