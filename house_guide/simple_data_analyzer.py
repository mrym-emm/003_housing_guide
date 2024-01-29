import pandas as pd


class SimpleDataAnalyzer:

    """
    A class where a data file can be analyzed (in this case its a csv file)
    ...

    Attributes
    ----------

    path : str
        the path of the file

    Methods
    -------
    extract_property_info
        returns a pandas dataframe

    currency_exchange
        returns a NumPy array of transformed prices

    suburb_summary
        display the summary of the properties with respect to # of bedrooms, bathrooms & parking spaces

    avg_land_size
        tbc

    """


    def __init__(self, path = None):

        """
        Construts all necessary attritbutes for the SimpleDataAnalyzer object

        Parameters
        ----------
            path : str
                the path of the file that is to be analyzed (default is None)

        """

        self.path = path


    def extract_property_info(self, file_path):

        """
        For reading the property information from the data file at the specified file_path

        Parameters
        ----------
        file_path : str, required

        Returns
        -------
        return a panda dataframe

        References
        ----------
        Approach taken from Ass2 - CarRetailer class, line 151
        """

        #since a SimpleDataAnalyzer object has a 'path' attiribute, we can passed it tru the pd.read_csv function
        #unclean dataframe has 118771 rows & 20 columns
        dataframe = pd.read_csv(self.path)

        #removing all rows where price is NaN, checked if theres any NaN in price column using 'dataframe_clean['price'].isnull().sum()'
        dataframe_clean = dataframe[dataframe.price.notnull()]

        #is a panda dataframe type, and has 104833 rows & 20 columns
        return dataframe_clean


    def currency_exchange(self, dataframe, exchange_rate):

        """
        To exchange prices of customers from different countries. I use this method mostly in my DataVisualizer Class.

        Parameters
        ----------
        dataframe : pandas.core.frame.DataFrame, required
            this is the same dataframe retrieved from extract_property_info method

        exchange_rate : str, required
            will depend on customer's input based on the available options represented in the currency dictionary

        Returns
        -------
        a numpy array of the transformed prices

        References
        ----------
        Extract column from dataframe : https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html
        To transform the prices to target currency : https://www.geeksforgeeks.org/python-pandas-series-multiply/
        To change panda series to numpy array : https://www.statology.org/pandas-series-to-numpy-array/
        """

        #used the currency dictionary from assignment brief
        currency_dict = {"AUD": 1, "USD": 0.66, "INR": 54.25, "CNY": 4.72, "JPY": 93.87, "HKD": 5.12, "KRW": 860.92, "GBP": 0.51, "EUR": 0.60, "SGD": 0.88}

        #ensure the exchange rate matches in the dictionary
        exchange_rate = exchange_rate.upper()

        #get the value of the currecny from the dictionary
        exchange_rate_value = currency_dict.get(exchange_rate)

        #extracts the price column from the dataframe, this is type pandas series
        aud_price_column = dataframe['price']

        #converts the aud currency to the target currency
        user_price_column = aud_price_column.multiply(other = exchange_rate_value)

        #to convert the series to numpy array
        user_price_column_array = user_price_column.to_numpy()

        #is a numpy array type --> <class 'numpy.ndarray'>
        return user_price_column_array


    def transformed_price_dataframe(self, dataframe, exchange_rate):

        """
        This is a method to return a dataframe that has the converted price. It will take the numpy array of from the-
        -currency_exchange method and convert it to a series to later add to existing dataframe.

        Parameters
        ----------
        dataframe : pandas.core.frame.DataFrame, required
            this is the same dataframe retrieved from extract_property_info method

        exchange_rate : str, required
            will depend on customer's input based on the available options represented in the currency dictionary

        Returns
        -------
        an updated dataframe with a new 'conv_price' column

        Reference
        ---------
        Python Pandas Tutorial (Part 3): Indexes - How to Set, Reset, and Use Indexes : https://www.youtube.com/watch?v=W9XjRYFkkyw&t=773s&ab_channel=CoreySchafer
        pandas.DataFrame.index: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.index.html
        to correct alignment of the new column: https://www.dataquest.io/blog/tutorial-indexing-dataframes-in-pandas/
        adding column to dataframe : https://builtin.com/data-science/pandas-add-column
        """

        #adding the coverted price column to the existing dataframe, and setting column name
        series_to_add = pd.Series(self.currency_exchange(dataframe, exchange_rate), index=dataframe.index)
        dataframe['conv_price'] = series_to_add

        return dataframe


    def suburb_summary(self, dataframe, suburb):

        """
        To display the summary of properties with respect to # bedrooms, bathrooms & parking spaces
        My approach to this method is to first know what suburb is in the csv file and then use conditional statements to-
        -tie everything together. Filter approach was referred to Corey Schaffer's video

        Parameters
        ----------
        dataframe : pandas.core.frame.DataFrame, required
            this is the same dataframe retrieved from transformed_price_dataframe method

        suburb : str, required
            will depend on customer's input based on which suburb they want

        Returns
        -------
        displays the mean, std.dev, median, min & max values of the mentioned items before
        if value of suburb is 'all', then will display summary of ALL suburb
        if value of suburb is specified, then will display summary of SPECIFIED suburb
        if value of suburb does not exist in file, then error message

        References
        ----------
        Filtering approach (at minute 10) : https://www.youtube.com/watch?v=Lw2rlcxScZY&t=1150s&ab_channel=CoreySchafer
        Finding unique values in series : https://www.projectpro.io/recipes/list-unique-values-in-pandas-dataframe
        Mapping function used : https://stackoverflow.com/questions/1801668/convert-a-list-with-strings-all-to-lowercase-or-uppercase
        Finding exact match in series : https://stackoverflow.com/questions/45164537/filter-pandas-data-frame-based-on-exact-string-match
        Basic stats for summary : https://stackoverflow.com/questions/19124148/modify-output-from-python-pandas-describe
        """

        #extracting all unique values in suburb column and converting all of them to lowercase
        all_suburb = dataframe['suburb'].unique()
        lower_all_suburb = list(map(lambda x: x.lower(), all_suburb))

        #ensuring user input is lowercased to match element in lower_all_suburb
        suburb = suburb.lower()

        #if target suburb is not in the lower_all_suburb then perform code for 'all' and non-existant suburbs
        if suburb not in lower_all_suburb:

            #if user inputs all
            if suburb == "all":

                spec_dataframe = dataframe[['bedrooms', 'bathrooms', 'parking_spaces']]

                print(f"     📜Below is a summary for {suburb.upper()} suburbs📜\n")

                return round(spec_dataframe.describe().loc[['mean','std','50%','min','max']], 2)

            #if suburb does not exist
            else:
                pass

                fsuburb = suburb.title()
                return f"Sorry. {fsuburb} not found. Please try another suburb ☹"

        #code for any specified suburb
        else:

            #to match suburb in the original values in the dataframe, i converted them to title case
            suburb = suburb.title()

            #from the 'suburb' column, match the target suburb and save it in a variable
            #this will always be true because this whole 'else' block of code is based if the target suburb is in the lower_all_suburb
            filt = dataframe['suburb'] == suburb

            #extracting the columns based on the filter
            df_to_summarize = dataframe.loc[filt]

            spec_dataframe = df_to_summarize[['bedrooms', 'bathrooms', 'parking_spaces']]

            print(f"\n    📜Below is a summary for properties in {suburb.title()}📜\n")

            return round(spec_dataframe.describe().loc[['mean', 'std', '50%', 'min', 'max']], 2)



    def avg_land_size(self, dataframe, suburb):

        """
        This method is to return the overall land size of properties in a suburb. If a user enters a suburb, and there-
        -are 10 properties in that suburb, the method will return the average land size of all properties in that specific suburb.

        Parameters
        ----------
        dataframe : pandas.core.frame.DataFrame, required
            this is the same dataframe retrieved from transformed_price_dataframe method

        suburb : str, required
            will depend on customer's input based on which suburb they want

        Returns
        -------

        if value of suburb is 'all', then will return avg land size of ALL suburb
        if value of suburb is specified, then will return avg land of SPECIFIED suburb
        if value of suburb does not exist in file, then error message

        References
        ----------

        Exc Rows: https://saturncloud.io/blog/how-to-exclude-rows-from-a-pandas-dataframe-based-on-column-value-and-not-index-value/
        """

        #extracting all unique values in suburb column and converting all of them to lowercase
        all_suburb = dataframe['suburb'].unique()
        lower_all_suburb = list(map(lambda x: x.lower(), all_suburb))

        #ensuring user input is lowercased to match element in lower_all_suburb
        suburb = suburb.lower()

        #excluding rows of data where land_size is invalid ie. -1
        exc_dataframe = dataframe[dataframe['land_size'] >= 1]
        land_size_property = exc_dataframe['land_size']

        if suburb not in lower_all_suburb:

            if suburb == "all":

                #getting the mean of ALL land size in hectar metres & converting it to meters
                conv_avg_land_size = round(land_size_property.mean() * 10000, 2)


                return f"The average land size for ALL suburb is {conv_avg_land_size} m2"

            else:

                #display message if suburb does not exist
                fsuburb = suburb.title()
                return f"Sorry. There are no properties in {fsuburb}. Please try another suburb ☹"

        else:

            #ensure the suburb that is passed tru matched the ones in the dataframe
            suburb = suburb.title()

            #filter dataframe based on the suburb
            filt = dataframe['suburb'] == suburb
            df_to_summarize = dataframe.loc[filt]

            #excluding rows of data where land_size is invalid ie. -1
            exc_dataframe = df_to_summarize[df_to_summarize['land_size'] >= 1]
            land_size_property = exc_dataframe['land_size']

            #Based on google, to convert hectar meter to meter, must multiply by 10000
            converted_land_meters = land_size_property.multiply(other = 10000)

            #getting average and rounding it 2 decimal places
            avg_ext_land_size = round(converted_land_meters.mean(), 2)

            return f"The average land size in {suburb} is {avg_ext_land_size} m2"


    def locate_price(self, target_price, data, target_suburb):

        """
        This method is a specific price in the dataframe. The method will essentially extract the suburb & conv_price-
        -column and then group them by the target suburb. This will then extract the conv_price column and transform-
        -it into a list and will apply a 'reverse insertion sort' on the list. Later a binary search will be applied-
        -to the reversed list, to search for the target price. The approach of this method uses an inner function and-
        -since it has to be recursive. Reverse insertion and recursive binary code is cited in references

        Parameters
        ----------

        target_price : float, required
            will depend on customer's input based on which price they want to search

        data : pandas.core.frame.DataFrame, required
            this is the same dataframe retrieved from transformed_price_dataframe method

        target_suburb : str, required
            will depend on customer's input based on which suburb they want to search

        Returns
        -------

        True if target_price is found
        False if target_price is not found

        References
        ----------

        1. reverse insertion : https://letsfindcourse.com/coding-questions/insertion-sort-program-descending-order
        2. How do I insertion sort a list of lists? : https://stackoverflow.com/questions/36863697/how-do-i-insertion-sort-a-list-of-lists
        3. list to dataframe: https://www.geeksforgeeks.org/create-a-pandas-dataframe-from-lists/
        4. The Binary Search : https://edstem.org/au/courses/12858/lessons/40660/slides/281845
        5. The Binary Search : https://www.youtube.com/watch?v=7nbatZEehyo&ab_channel=CodingwithEstefania
        6. Inner function in method: https://codereview.stackexchange.com/questions/102705/recursive-binary-search-in-python
        7. Multiply each element in a list by a number using map(): https://bobbyhadz.com/blog/python-multiply-each-element-in-list-by-number
        """

        target_suburb = target_suburb.title()

        ext_column = data[['suburb', 'conv_price']]

        clean_ext_column = ext_column.dropna()

        suburb_group = clean_ext_column.groupby(['suburb'])

        target_suburb_group = suburb_group.get_group(target_suburb)

        price_array = target_suburb_group['conv_price']

        target_price_by_suburb = price_array.tolist()

        n = len(target_price_by_suburb)

        #Below reverse insertion sort code was adjusted and was retrieved from (2) from reference
        for step in range(1, n):
            key = target_price_by_suburb[step]
            j = step - 1
            while j >= 0 and key > target_price_by_suburb[j]:

                # For descending order
                target_price_by_suburb[j + 1] = target_price_by_suburb[j]
                j = j - 1
            target_price_by_suburb[j + 1] = key

        price_data = target_price_by_suburb

        # Below recursive binary search code was adjusted and was retrieved from (5) & (6) from reference
        low = 0
        high = len(price_data) - 1


        #inner function approach
        def binary(price_data, low, high, target_price):

            if low <= high:

                middle = (low + high) // 2

                if price_data[middle] == target_price:

                    return True

                elif target_price > price_data[middle]:

                    return binary(price_data, low, middle - 1, target_price)

                else:
                    return binary(price_data, middle + 1, high, target_price)

            return False

        #calls inner function to execute it
        return binary(price_data, low, high, target_price)


    def get_rows_of_specific_price(self,target_price, data, target_suburb):

        """
       This method is an additional method that uses the locate_price method and returns the row of properties that mathcse target_prices

       Parameters
       ----------

       target_price : float, required
           will depend on customer's input based on which price they want to search

       data : pandas.core.frame.DataFrame, required
           this is the same dataframe retrieved from transformed_price_dataframe method

       target_suburb : str, required
           will depend on customer's input based on which suburb they want to search

       Returns
       -------

       if locate_price == True, it will return rows in a dataframe where conv_price matches target_price
       else, a message informing user that price does not match will be displayed

       References
       ----------
       Filter Pandas Dataframe with multiple conditions: https://www.geeksforgeeks.org/filter-pandas-dataframe-with-multiple-conditions/
       Python Pandas Tutorial (Part 4): Filtering - Using Conditionals to Filter Rows and Columns: https://www.youtube.com/watch?v=Lw2rlcxScZY&t=1150s&ab_channel=CoreySchafer

       """

        if self.locate_price(target_price, data, target_suburb) == True:

            #ensure that user_input is converted to float to do comparison
            target_price = float(target_price)

            #filtering out the dataframe to those that matches the target_suburb and conv_price. In pandas they use '&' for 'and' and '|' for 'or'
            searched_dataframe = data[(data['suburb'] == target_suburb.title()) & (data['conv_price'] == target_price)]

            #create variable to display dataframe of selected columns to display to user
            dataframe_to_display = searched_dataframe[['id', 'suburb', 'bedrooms', 'bathrooms', 'parking_spaces','conv_price']]

            return dataframe_to_display

        else:
            return f"No properties to display matching that price"
