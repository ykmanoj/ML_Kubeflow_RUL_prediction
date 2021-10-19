import argparse
import json
import os
import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(1337)
import requests, zipfile
from io import BytesIO
import pickle
#from tensorflow import gfile


def _collect_data(args):

    r = requests.get('https://ti.arc.nasa.gov/c/6/', stream=True)
    z = zipfile.ZipFile(BytesIO(r.content))
    z.extractall()

    train1 = pd.read_csv('train_FD001.txt', parse_dates=False, delimiter=" ", decimal=".", header=None,index_col=0)
    test1 = pd.read_csv('test_FD001.txt', parse_dates=False, delimiter=" ", decimal=".", header=None,index_col=0)
    RUL1 = pd.read_csv('RUL_FD001.txt', parse_dates=False, delimiter=" ", decimal=".", header=None,index_col=0)


    train2 = pd.read_csv('train_FD002.txt', parse_dates=False, delimiter=" ", decimal=".", header=None,index_col=0)
    test2 = pd.read_csv('test_FD002.txt', parse_dates=False, delimiter=" ", decimal=".", header=None,index_col=0)
    RUL2 = pd.read_csv('RUL_FD002.txt', parse_dates=False, delimiter=" ", decimal=".", header=None,index_col=0)

    train3 = pd.read_csv('train_FD003.txt', parse_dates=False, delimiter=" ", decimal=".", header=None,index_col=0)
    test3 = pd.read_csv('test_FD003.txt', parse_dates=False, delimiter=" ", decimal=".", header=None,index_col=0)
    RUL3 = pd.read_csv('RUL_FD003.txt', parse_dates=False, delimiter=" ", decimal=".", header=None,index_col=0)

    train4 = pd.read_csv('train_FD004.txt', parse_dates=False, delimiter=" ", decimal=".", header=None,index_col=0)
    test4 = pd.read_csv('test_FD004.txt', parse_dates=False, delimiter=" ", decimal=".", header=None,index_col=0)
    RUL4 = pd.read_csv('RUL_FD004.txt', parse_dates=False, delimiter=" ", decimal=".", header=None,index_col=0)

    print(train1.head())
    # Creates `data` structure to save and
    # share train and test datasets.
    data = {'train1': train1,
            'test1': test1,
            'RUL1': RUL1,

            'train2': train2,
            'test2': test2,
            'RUL2': RUL2,

            'train3': train3,
            'test3': test3,
            'RUL3': RUL3,

            'train4': train4,
            'test4': test4,
            'RUL4': RUL4
            }

    # Creates a json object based on `data`
    #data_json = json.dumps(data)
    pickle_file = 'full_data.pickle'

    with open(args.output_data+'/'+pickle_file, 'wb') as downloaded_data:
        pickle.dump(data, downloaded_data)
    
if __name__ == '__main__':
    # This component does not receive any input
    # it only outpus one artifact which is `data`.
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_data', type=str)

    args = parser.parse_args()
    print(args)
    Path(args.output_data).parent.mkdir(parents=True, exist_ok=True)

    _collect_data(args)
