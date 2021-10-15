import argparse
import json
import os
import pandas as pd
import numpy as np
from kfp.components import create_component_from_func
from path import Path

np.random.seed(1337)
import requests, zipfile, StringIO


def _collect_data():

    r = requests.get('https://ti.arc.nasa.gov/c/6/', stream=True)
    z = zipfile.ZipFile(StringIO.StringIO(r.content))
    z.extractall()

    train = pd.read_csv('train_FD001.csv', parse_dates=False, delimiter=" ", decimal=".", header=None)
    test = pd.read_csv('test_FD001.csv', parse_dates=False, delimiter=" ", decimal=".", header=None)
    RUL = pd.read_csv('RUL_FD001.csv', parse_dates=False, delimiter=" ", decimal=".", header=None)

    # Creates `data` structure to save and
    # share train and test datasets.
    data = {'train': train.tolist(),
            'test': test.tolist(),
            'RUL': RUL.tolist()
            }

    # Creates a json object based on `data`
    data_json = json.dumps(data)

    # Saves the json object into a file
    with open(args.data, 'w') as out_file:
        json.dump(data_json, out_file)


if __name__ == '__main__':
    # This component does not receive any input
    # it only outpus one artifact which is `data`.
    parser = argparse.ArgumentParser()
    #parser.add_argument('--data', type=str)

    args = parser.parse_args()

    # Creating the directory where the output file will be created
    # (the directory may or may not exist).
    #Path(args.data).parent.mkdir(parents=True, exist_ok=True)

    _collect_data()

    # download_op = create_component_from_func(
    #         _collect_data,
    #         output_component_file='collect_data.yaml',  # optional
    #         base_image='python:3.6',  # Optional
    #         packages_to_install=['pandas==0.24'],  # Optional
    # )

    # The component spec can be accessed through the .component_spec attribute:
    # download_op.component_spec.save('download_data.yaml')
