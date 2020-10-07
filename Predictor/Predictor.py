# Author : Richard Delwin Myloth

import numpy as np
import pickle
import re
import pandas as pd
from subprocess import check_output
from Features.feature_extraction import Size, Key, Authors
import Training.Pre_processing as pre
from sys import exit

# To handle Settings Warning
pd.set_option('mode.chained_assignment', None)


def load_model(model_filename):
    """
    This function is used to load the trained model for prediction from the specified file location.

    :param model_filename: Location of the trained model (String)
    :return: model instance
    """
    with open(model_filename, 'rb') as file:
        model = pickle.load(file)

    return model


def predict(data, model):
    """
    For predicting the risk index of the commit.

    :param data: numpy array containing the attribute values for the commit.
    :param model: model created by invoking load_model
    :return: Probability of risk
    """
    return model.predict_proba(data)


def get_latest_commit_details():

    """
    This function is called to obtain the latest commit by executing the git bash command.
    However, this function is not used since the python script handles this part.

    :return: The output resulting on executing the git bash command
    """
    bash_cmd = 'git log -1 --pretty=format:"%an%n%s%n" --shortstat'
    stdout = check_output(bash_cmd.split()).decode('utf-8').rstrip('\n')
    return stdout


def extract_info(stdout):

    """
    This function is called to structure the data received on executing the git bash command.
    The author, commit message, number of lines, lines added and lines deleted, files changes are extracted from it and
     converted into a pandas.DataFrame. Later,the message length is also added to it.

     First it checks if the length of the stdout array is less than 4, if so it indicates that no files were changed
     hence it cannot predict the risk index due to insufficient data.

    :param stdout:
    :return:
    """
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
    """
    This function is used to convert the pandas.DataFrame into a numpy array and reshape into the dimension of (1,6)
    i.e. (rows, columns) so that the model is able to process it

    :param stdout: DataFrame containing the attribute values
    :return: np.ndarray of dimension (1,6)
    """

    stdout = np.reshape(np.array(stdout), (1, 6))
    return stdout


def process_df(df):
    """
    This function is used to convert the data such as commit messages, author names into an array of keywords
    and/or map it to intger values or label encode them.
    :param df:
    :return:
    """

    commit_msg = Key(df)
    resp = commit_msg.map_keywords_to_val("comment")
    authors = Authors(df, "author")
    pre.Label_encode(df)
    return
