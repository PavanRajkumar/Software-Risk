"""
@author : Richard Delwin Myloth

"""
class AuthorDetails:

    """
    This class is concerned with extracing author names and other info : -
    Done:
        extract names

    Additional:
        * extract number of commits for an author
    """

    def __init__(self, data):

        """
        :param data: the dataframe consisting of the author names column from
         which the author_names are extracted and cleaned inplace (type - pandas.DataFrame)
        """
        self.data = data


    def get_author_names(self, column_name="author"):
        """

        :param column_name: should be author, indicates the column on which the functions acts upon (type - String)
        :return: all distinct authors (type list)
        """

        print(">>Extracting author names<<")
        author_names = []
        for row_num in range(self.data.shape[0]):

            name = self.data[column_name].iloc[row_num]
            name = name.strip()
            author_names.append(name)
        return author_names

    def get_number_of_commits(self):

        """
        To be done

        Intended to extract new data regarding the number of commits for every author so that it could
        also be considered as a parameter when creating the ML model to assess the risk of a commit
        :return: None
        """
        pass

