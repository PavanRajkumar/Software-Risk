""""
@author : Richard Delwin Myloth
"""

import string
import re
from Features.author_details import AuthorDetails
import random


# Used to extract numeric data 
# input : dataframe and column name
class Size:

    """
    This class is used to remove non-numeric data, leaving behind only numeric data
    also accounts for removing whitespaces which might be present for merge commits
    """

    def __init__(self, data):
        """
        :param data: the dataframe consisting of the columns -
         * files changed
         * lines added
         * lines deleted
         from which non-numeric data are removed inplace (type - pandas.DataFrame)
        """
        self.data = data

    def keep_numeric_data(self, column_name):

        """

        :param column_name: could be (intended for) files changed, lines added, lines deleted
            but can also be used for any other column which is supposed to be having only numeric data
            (type - String)
        :return: None
        """

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

        return



class Key:
    """
    To extract keywords from the commit messages
    # the keywords classified into five categories
        # 1. corrective ("fix""bug", "wrong", "fail", "problem")
        # 2. addition, ("new", "add", "requirement", "initial", "create")
        # 3. non functional ("doc", "merge")
        # 4. perfective ("clean", "better")
        # 5. preventive ("test", "junit", "coverage", "assert")
    """

    def __init__(self, data):

        """
            :param data: the dataframe consisting of the commit messages from
             which the keywords are extracted, mapped to integer values and cleaned inplace (type - pandas.DataFrame)
        """


        self.data = data

        self.keywords = {"fix": 9, "bug": 9, "wrong": 9, "fail": 9, "problem": 9, "imp": 8,
                         "new": 7, "add": 7, "requirement": 7, "initial": 7, "create": 7,
                         "doc": 2, "merge": 2,
                         "clean": 3, "better": 3,
                         "test": 1, "junit": 1, "coverage": 1, "assert": 1,
                         }

    def map_keywords_to_val(self, column_name):
        """

        :param column_name: comment (type - String)
        :return: None

        The commented parts: -
        + Lines are commented to just find the keywords and sort them rather than assigning values
        """
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
    """
        This class is concerned with extracting author names and mapping them to a numeric value

        ******************************************************************************************************
        ** However this class isn't used, instead the author_details.py is used to just clean author names ***
        ******************************************************************************************************

        Done:
            extract names
            map values from distinct string to integers

        Additional:
            * extract number of commits for an author
        """


    def __init__(self, data, column_name):
        """

        :param data: The DataFrame consisting of authors
        :param column_name: author
        """

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

        """
        This function was intended to clean author names and map them to integer values
        which could have been an indication for author commit experience, author's seniority etc.
        :return: Dictionary of authors

        """

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
