# Author : Richard Delwin Myloth

# This piece of code extracts the author names from a dataframe. 

class AuthorDetails:

    def __init__(self, data):
        self.data = data


    def get_author_names(self, column_name):

        print(">>Extracting author names<<")
        author_names = []
        for row_num in range(self.data.shape[0]):

            name = self.data[column_name].iloc[row_num]
            name = name.strip()
            author_names.append(name)
        return author_names

    def get_number_of_commits(self):
        pass

