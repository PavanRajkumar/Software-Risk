
from sklearn.preprocessing import LabelEncoder
from scipy import stats
import numpy as np
import pandas as pd

def Label_encode(data):
    """
        This function is used to label encode comment and author names (inplace). This is used now but can be
        substituted by the function in Features directory which maps to numeric values.

    :param data: Training data (type - pandas.DataFrame)
    :return: None
    """

    lb_make = LabelEncoder()
    data["comment"] = lb_make.fit_transform(data["comment"])
    data["author"] = lb_make.fit_transform(data["author"])

    data.reset_index(drop=True, inplace=True)

    return


def remove_non_numeric_data(data):
    """
    This function is used to remove non-numeric data (inplace) which might be present (quite rare) in
    the column intended for numeric data.

    :param data: The training data (type - pandas.DataFrame)
    :return: None
    """
    del_ind = []
    for row_num in range(data.shape[0]):
        ele = data["changed files"].iloc[row_num]
        if ele == " ":
            data["changed files"].iloc[row_num] = 0
        elif not str(ele).isdigit():
            del_ind.append(row_num)
    print("Number of non numeric instances removed", len(del_ind))
    data.drop(del_ind, inplace=True)
    data['changed files'] = pd.to_numeric(data['changed files'])
    return


def removing_outliers(data):
    """
    This function is used to remove any outliers in the data. They generally emerge from the commit by bots
    which tend to have a very large number of lines added due to formatting.

    :param data: the DataFrame containing the attributes an dthe target variable
    :return: None
    """

    print(data.info())
    z = np.abs(stats.zscore(data))
    threshold = 3

    indexes, rows = np.where(z > threshold)
    indexes = list(set(indexes))

    # print(len(indexes))
    z, o = 0, 0

    for i in indexes:
        if data["buggy"].iloc[i] == 0:
            z += 1
        else:
            o += 1
    orig_rows = data.shape[0]

    for ind in indexes:
        data.drop(ind, inplace=True)

    print("Number of instances removed : ", orig_rows - data.shape[0])

    return