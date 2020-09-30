# Author : Richard Delwin Myloth

import numpy as np
import pickle
import re
import pandas as pd
from subprocess import check_output
from Features.feature_extraction import Size, Key, Authors
import Training.Pre_processing as pre
from sys import exit


#To handle Settings Warning
pd.set_option('mode.chained_assignment', None)


def load_model(model_filename):

    with open(model_filename, 'rb') as file:
        model = pickle.load(file)

    return model

def predict(data, model):

    return model.predict_proba(data)

def get_latest_commit_details():

    bash_cmd = 'git log -1 --pretty=format:"%an%n%s%n" --shortstat'
    stdout = check_output(bash_cmd.split()).decode('utf-8').rstrip('\n')
    return stdout

def extract_info(stdout):

    stdout = stdout.split("\n")

    if len(stdout) < 4:
        print("-----------------")
        print(stdout)
        return "Cannot analyse, no files changed"

    stdout[0] = stdout[0].replace('"', "")
    stdout[1] = stdout[1].replace('"', "")
    temp = re.findall(r'\s\d+\s', stdout[-1])
    res = list(map(int, temp))
    if len(res) == 1:
        res.append(0)
        res.append(0)
    elif len(res) == 2:
        res.append(0)

    stdout = stdout[:2] + res
    msg_len = len(stdout[1])
    stdout.append(msg_len)

    stdout = reshape_np(stdout)
    return stdout

def reshape_np(stdout):
    stdout = np.reshape(np.array(stdout), (1, 6))
    return stdout

def process_df(df):
    commit_msg = Key(df)
    resp = commit_msg.map_keywords_to_val("comment")
    authors = Authors(df, "author")
    pre.Label_encode(df)
    return
