# Author : Richard Delwin Myloth


import string
import re
from .author_details import AuthorDetails
import random


# Used to extract numeric data 
# input : dataframe and column name
class Size:

    def __init__(self, data):
        self.data = data

    def keep_numeric_data(self, column_name):

        for row_num in range(self.data.shape[0]):

            numeric_data = ""
            error_ = False

            if self.data[column_name].iloc[row_num] != 'nan':

                row_value = str(self.data[column_name].iloc[row_num]).strip()

                try:
                    numeric_data = int(row_value[:row_value.index(" ")])
                except ValueError as v:
                    error_ = True

                if not error_ and numeric_data:
                    self.data[column_name].iloc[row_num] = int(numeric_data)

        return 1


# To extract keywords from the commit messages
# input : dataframe
class Key:

    def __init__(self, data):

        # the keywords classified into five categories
        # 1. corrective ("fix""bug", "wrong", "fail", "problem")
        # 2. addition, ("new", "add", "requirement", "initial", "create")
        # 3. non functional ("doc", "merge")
        # 4. perfective ("clean", "better")
        # 5. preventive ("test", "junit", "coverage", "assert")
        self.data = data

        self.keywords = {"fix": 9, "bug": 9, "wrong": 9, "fail": 9, "problem": 9, "imp": 8,
                         "new": 7, "add": 7, "requirement": 7, "initial": 7, "create": 7,
                         "doc": 2, "merge": 2,
                         "clean": 3, "better": 3,
                         "test": 1, "junit": 1, "coverage": 1, "assert": 1,
                         }

    def map_keywords_to_val(self, column_name):

        #Lines are commented to just find the keywords and sort them rather than assigning values

        i = 0
        z = 0
        self.data["msg_len"] = [0 for _ in range(self.data.shape[0])]

        for row_num in range(self.data.shape[0]):

            keys_in_msg = []
            message = self.data[column_name].iloc[row_num]

            if str(message) == "nan":
                continue

            len_msg = len(message)
            message = message.lower().strip()
            message = message.translate(str.maketrans('', '', string.punctuation))
            message = re.sub(" +", " ", message).split(" ")

            for key in self.keywords.keys():
                if key in message:
                    keys_in_msg.append(key)

            # val = 0
            # if keys_in_msg:
            #     for key in keys_in_msg:
            #         val += self.keywords[key]

            keys_in_msg.sort()

            self.data[column_name].iloc[row_num] = " ".join(keys_in_msg)
            # self.data[column_name].iloc[row_num] = val
            # i += 1
            # if val == 0:
            #     z += 1

            self.data["msg_len"].iloc[row_num] = len_msg

        return #{"modified rows": i, "zero values": z, "non zero": i - z}


# To map authors to randomly assigned experience values
class Authors:

    # author commit exp, auth seniority
    def __init__(self, data, column_name):
        self.data = data
        self.column_name = column_name
        # author = AuthorDetails(self.data)
        # self.author_names = author.get_author_names(column_name)

        self.author_names = self.data[column_name].unique()
        self.author_rating = {}

        for name in self.author_names:
            self.author_rating[name] = random.randint(2, 20)
        self.author_rating["RichardDelwin"] = 12

    def map_author_to_val(self):
        i = 0
        for row_num in range(self.data.shape[0]):

            author_name = self.data.author.iloc[row_num]

            if author_name in self.author_rating:
                val = self.author_rating[author_name]
                self.data.author.iloc[row_num] = val
            else:
                i += 1
                # print("Author not found in dictionary")

        return {"Authors not accounted": i, "Total Authors": len(self.author_names)}
