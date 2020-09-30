# Author : Richard Delwin Myloth
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import pickle
from imblearn.under_sampling import RandomUnderSampler
from collections import Counter
from sklearn.metrics import accuracy_score, recall_score, precision_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split

def undersample(X, y):

    print("Before undersampling : Dataset  = ", Counter(y))

    rus = RandomUnderSampler(random_state=42)
    X, y = rus.fit_resample(X, y)
    print("After undersampling : Dataset  = ", Counter(y))

    return

def create_model():
    data = pd.read_csv("./cleaned_data_latest.csv",
                       names=list(
                           "author,comment,changed files,lines added,lines deleted,msg_len,buggy".split(",")))

    data = data[1:]

    # print(data[data.isnull().any(axis=1)])
    data.dropna(inplace=True)
    data.fillna(data.mean(), inplace=True)
    y = data["buggy"]
    X = data.drop(columns=["buggy"], axis=1)
    undersample(X, y)

    ##for model stats
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print("Accuracy : ", accuracy_score(y_test, y_pred)*100)
    print("Confusion matrix: \n", confusion_matrix(y_test, y_pred))
    # print("Recall : ", recall_score(y_test, y_pred))
    # print("Precision : ", precision_score(y_test, y_pred))
    # print("F1_score : ", f1_score(y_test, y_pred))

    clf = RandomForestClassifier(random_state=40)
    clf.fit(X, y)

    pkl_filename = "rf_model_del.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(clf, file)

    print(">>Model Saved<<")

create_model()


