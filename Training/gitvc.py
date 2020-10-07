"""
@Author: Richard Delwin Myloth, Pavan Rajkumar

Gitvc.ipynb

Colaboratory File (used for prototyping):
https://colab.research.google.com/drive/1MP0cSkbEu9bgC1NkQLKZy1Elgdqmag8c

"""

import pandas as pd
from Training.parsing import get_labels
from Training.create_model import create_model
import Features.feature_extraction as features
import Training.Pre_processing as pre
import ast
from collections import Counter


def remove_merge_commits(data):
    """
        Removes those commits (inplace) which are introduced due to merging of branches.
        These commits does not contribute any information
    :param data: The DataFrame containg the raw data extracted by executing the git command (type - pandas.DataFrame)
    :return: None
    """
    data = data[data["author"] != "Odoo's Mergebot"]
    data[~data['comment'].str.contains('[MERGE]', na=False)]


# print("The shape of data :", data.shape)
# Extract numeric features by using function
# defined in /Features/feature_extraction.py
def extract_num():
    """
    To converted numbers represented as a String into numeric values
    :return: None

    """
    print(">> Extracting numeric values <<\n")
    data['lines added'] = pd.to_numeric(data['lines added'])
    data['lines deleted'] = pd.to_numeric(data['lines deleted'])

    # data['changed files'] = pd.to_numeric(data['changed files'])
    # size_features = features.Size(data)
    # size_features.keep_numeric_data("changed files")
    # size_features.keep_numeric_data("lines deleted")
    # size_features.keep_numeric_data("lines added")


# assigning values to keywords
# Extract keywords and map them to values by
# using function defined in /Features/feature_extraction.py
# assigning values to keywords
def extract_keywords():
    """
    This function is used to extract keywords from commit messages and to map them to a numeric value.

    :return: None

    """
    print(">> Extracting keywords from commit <<\n")
    # print(resp)
    commit_msg = features.Key(data)
    resp = commit_msg.map_keywords_to_val("comment")


# assigning values to authors
# Mapping author to experience values
# by using function defined in /Features/feature_extraction.py
def map_authors():
    """
    This function is used to map authors to certain numeric values by invoking authors
    :return:
    """
    print(">> Mapping Authors <<\n")
    authors = features.Authors(data, "author")
    resp = authors.map_author_to_val()
    print(resp)


def fill_na():
    """
    To fill missing values with 0 for columns containing numeric data

    :return: None
    """
    print(">> Filling na values <<\n")
    data["changed files"].fillna(0, inplace=True)
    data["lines added"].fillna(0, inplace=True)
    data["lines deleted"].fillna(0, inplace=True)
    data["comment"].fillna("", inplace=True)
    num_of_na = data.isnull().sum()


def misc():
    """
    This function is used to remove certain instances which are unique to a repository.
    This functiion is not used since it is handled by git commands.
    :return: None
    """
    data.loc[data['changed files'] == " ", 'changed files'] = 0
    data.drop(data[data['changed files'] == 'account: use reply_to header from tmplt""'].index, inplace=True)
    data.loc[data['lines added'] == " 0 insertions(+)", 'lines added'] = 0
    data.loc[data['lines deleted'] == " 0 deletions(-) ", 'lines deleted'] = 0


def label_bugs():
    """
    This function is used to invoke the Training.parsing.get_labels() to obtain the buggy commit_id
    which are mapped to raw data to create the target attribute. All non-buggy commits are labelled as
    0 and buggy commits are labelled as 1. The resulting new column is created inplace.

    :return: None
    """
    # Old code
    # buggy_commits = get_labels()
    # with open("./buggy.txt", "w+") as bugs:
    #     bugs.write(buggy_commits)

    #
    # buggy_commits = [bug[:5] for bug in buggy_commits]
    #
    # ins = [0 for _ in range(data.shape[0])]
    # data['buggy'] = ins
    #
    # for i in range(data.shape[0]):
    #     if str(data["commit id"].iloc[i])[:5] in buggy_commits:
    #         data["buggy"].iloc[i]=1

    buggy_commits = ""
    buggy_commits_2 = ""
    with open("../Git_logs/bug_test.txt", "r") as bugs:
        buggy_commits = bugs.read()

    with open("../Git_logs/bug_test_2.txt", "r") as bugs:
        buggy_commits_2 = bugs.read()

    buggy_commits = ast.literal_eval(buggy_commits)
    buggy_commits = [ele.strip() for ele in buggy_commits]

    buggy_commits_2 = ast.literal_eval(buggy_commits_2)
    buggy_commits_2 = [ele.strip() for ele in buggy_commits_2]

    # print(buggy_commits[:5])
    # print(type(buggy_commits[1]))
    # print(buggy_commits[0][0])
    # print("no of buggy file = ", len(buggy_commits))
    buggy_commits.extend(buggy_commits_2)
    print("no of buggy file = ", len(buggy_commits))

    buggy_commits = [bug[:8] for bug in buggy_commits]

    ins = [0 for _ in range(data.shape[0])]
    data['buggy'] = ins
    bugs = 0
    for i in range(data.shape[0]):
        if str(data["commit id"].iloc[i])[:8] in buggy_commits:
            bugs += 1
            data["buggy"].iloc[i] = 1
    print("\n bugs = ", bugs)

    return


def save_dataset(DATASET_LOCATION="./cleaned_data_latest.csv"):
    """
    This function is used to save the csv file pre-processsing so that it could be used to train the model.
    :return: None
    """

    # DATASET_LOCATION = "./cleaned_data_latest.csv"
    data.to_csv(DATASET_LOCATION, index=False)


if __name__ == "__main__":
    """The driver code
    """

    # To handle Settings Warning
    pd.set_option('mode.chained_assignment', None)

    # Read uncleaned CSV file
    data = pd.read_csv("../Git_logs/data_odoo_2.csv",
                       index_col=False,
                       names=list(
                           "commit id,author,date,comment,changed files,lines added,lines deleted".split(",")))

    data.drop(columns=["date"], axis=1, inplace=True)

    remove_merge_commits(data)
    extract_keywords()
    # map_authors()

    data_info = data.info()
    num_of_na = data.isnull().sum()

    fill_na()
    # misc()

    data = data.iloc[1:, :]
    label_bugs()
    data.drop(columns=["commit id"], axis=1, inplace=True)

    extract_num()
    pre.remove_non_numeric_data(data)
    pre.Label_encode(data)
    pre.removing_outliers(data)

    print(Counter(data["buggy"]))
    save_dataset()

    print(">>Creating Model<<")
    create_model()
