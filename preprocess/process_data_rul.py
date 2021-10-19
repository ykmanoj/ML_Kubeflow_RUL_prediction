# -*- coding: utf-8 -*-

import json
import pandas as pd
import numpy as np
import argparse
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pickle

def split(df):
    cols_normalize = df.columns.difference(['unit_number','time_in_cycles','RUL','label']) # NORMALIZE COLUMNS except [id , cycle, rul ....]
    X = df[cols_normalize]
    y = df['label']
   # if args.model=='classifier':
   #     y = df['label']
   # else:
   #     y = df['RUL']
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)
    return(X_train,X_test,y_train,y_test)

def scaling(X_train, X_test):
    min_max_scaler = MinMaxScaler()
    X_train_scaled = pd.DataFrame(min_max_scaler.fit_transform(X_train), columns=X_train.columns, index=X_train.index)
    X_test_scaled = pd.DataFrame(min_max_scaler.transform(X_test), columns=X_test.columns, index=X_test.index)
    return(X_train_scaled,X_test_scaled)

def remove_outliers(df):
    #train.drop(['s1', 's5', 's10', 's16', 's18', 's19', 'op_setting3'], axis=1, inplace=True)
    #test.drop(['s1', 's5', 's10', 's16', 's18', 's19', 'op_setting3'], axis=1, inplace=True)
    print(df.describe().transpose())

    df.drop(columns=['Nf_dmd','PCNfR_dmd','P2','P15','T2','TRA','farB','epr'],inplace=True)

    return df

def preprocessed(df):
    fd_RUL = df.groupby('unit_number')['time_in_cycles'].max().reset_index()
    fd_RUL = pd.DataFrame(fd_RUL)
    fd_RUL.columns = ['unit_number','max']
    df = df.merge(fd_RUL, on=['unit_number'], how='left')
    df['RUL'] = df['max'] - df['time_in_cycles']
    w=15
    df['label'] = np.where(df['RUL'] <= w,1,0)
    df.drop(columns=['max'],inplace = True)
    df = df[df['time_in_cycles']>0]
    return df

def process_data(args):

    print(args.input_data)
    with open(args.input_data,'rb') as data_file:
        data=pickle.load(data_file)

    print(data.keys())
    df_train = data['train1']
    df_test = data['test1']
    df_rul = data['RUL1']

    df_train.drop(df_train.columns[[-1,-2]], axis=1, inplace=True)
    df_test.drop(df_test.columns[[-1,-2]], axis=1, inplace=True)

    print('Data columns', df_train.columns)
    print(df_train.head())

    ### create labels
    columns = ['unit_number','time_in_cycles','setting_1','setting_2','TRA','T2','T24','T30','T50','P2','P15','P30','Nf','Nc','epr','Ps30','phi','NRf','NRc','BPR','farB','htBleed','Nf_dmd','PCNfR_dmd','W31','W32']
    df_train.columns = columns
    df_test.columns = columns

    train = remove_outliers(df_train)
    test = remove_outliers(df_test)

    df = preprocessed(train)
    
    X_train, X_test, y_train, y_test = split(df)
    X_train_scaled, X_test_scaled = scaling(X_train,X_test)
    X_train_scaled = X_train_scaled.to_numpy()
    X_test_scaled = X_test_scaled.to_numpy()

    print(df.head())
    data = {'x_train' : X_train_scaled,
            'y_train' : y_train,
            'x_test' : X_test_scaled,
            'y_test' : y_test}
    
    with open(args.output_data, 'wb') as out_file:
        pickle.dump(data, out_file)
    


if __name__ == '__main__':
    
    # This component does not receive any input
    # it only outpus one artifact which is `data`.
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_data', type=str)
    parser.add_argument('--output_data',type=str)

    args = parser.parse_args()
    print(args)

    # Creating the directory where the output file will be created 
    # (the directory may or may not exist).
    Path(args.output_data).parent.mkdir(parents=True, exist_ok=True)

    process_data(args)