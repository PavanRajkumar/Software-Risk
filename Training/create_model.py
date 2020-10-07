"""
@author : Richard Delwin Myloth
"""

from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import pickle
from imblearn.under_sampling import RandomUnderSampler
from collections import Counter
from sklearn.metrics import accuracy_score, recall_score, precision_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split


def undersample(X, y):
    """
    Undersampling of the dataset to balance the data to prevent bias. Especially in this scenario where the number
    of non-buggy commits might be far larger than buggy commits.

    :param X: The attributes (type = pandas.DataFrame)
    :param y: The target variable (type = pandas.DataFrame)
    :return:
    """

    print("Before undersampling : Dataset  = ", Counter(y))

    rus = RandomUnderSampler(random_state=42)
    X, y = rus.fit_resample(X, y)
    print("After undersampling : Dataset  = ", Counter(y))

    return


def create_model(MODEL_LOCATION="rf_model.pkl", DATA_LOCATION="./cleaned_data_latest.csv"):
    """
        Reads the csv file created containing the pre - processed training data.
        This functoin creates a RandomForest model and stores the created model
        as rf_model.pkl

        This function also calls create_model.undersample and drops those instances
        with missing values.

    :param MODEL_LOCATION: specifies the location of the model created
    :return: None

    """
    # MODEL_LOCATION = "rf_model.pkl"

    data = pd.read_csv(DATA_LOCATION,
                       names=list(
                           "author,comment,changed files,lines added,lines deleted,msg_len,buggy".split(",")))

    data = data[1:]

    # print(data[data.isnull().any(axis=1)])
    data.dropna(inplace=True)
    data.fillna(data.mean(), inplace=True)
    y = data["buggy"]
    X = data.drop(columns=["buggy"], axis=1)
    undersample(X, y)

    # for model stats

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print("Accuracy : ", accuracy_score(y_test, y_pred) * 100)
    print("Confusion matrix: \n", confusion_matrix(y_test, y_pred))
    # print("Recall : ", recall_score(y_test, y_pred))
    # print("Precision : ", precision_score(y_test, y_pred))
    # print("F1_score : ", f1_score(y_test, y_pred))

    clf = RandomForestClassifier(random_state=40)
    clf.fit(X, y)

    with open(MODEL_LOCATION, 'wb') as file:
        pickle.dump(clf, file)

    print(">>Model Saved<<")


create_model()
