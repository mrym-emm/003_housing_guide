import numpy as np
import matplotlib.pyplot as plt
from simple_data_analyzer import SimpleDataAnalyzer


class DataVisualizer(SimpleDataAnalyzer):

    """
    A class inheriting methods from SimpleDataAnalyzer to visualize the data analyzed
    ...

    Attributes
    ----------

    path : str
        Inherited from parent class SimpleDataAnalyzer

    Methods
    -------
    sales_trend
        saves a line chart of number of properties sold in each year. File that has the same name, will simply overwrite

    prop_val_distribution
        saves a histogram of the price distribution of properties in suburb / all suburbs. File that has the same name, will simply overwrite
    """

    def __init__(self, path = None):

        """
        Inherit attribute from SimpleDataAnalyzer parent class

        Parameters
        ----------
            path : str
                the path of the file to be visualized (default is None)
        """

        super().__init__(path)


    def sales_trend(self, dataframe):

        """
        Visualizes a line chart of number of property sold each year. The approach of this code needs a 'x' variable that is the year
        and a 'y' variable of the total number of properties.

        Parameters
        ----------
        dataframe : pandas dataframe, required

        Returns
        -------
        returns a message informing user that file has been saved in folder

        References
        ----------
        (1) extract substring from column: https://pandas.pydata.org/docs/reference/api/pandas.Series.str.extract.html
        (2) adding new column : https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/
        (3) Python Tutorial: re Module - How to Write and Match Regular Expressions (Regex): https://www.youtube.com/watch?v=K8L6KVGG-7o&ab_channel=CoreySchafer
        (4) dropping rows of NaN values in year column : https://stackoverflow.com/questions/46864740/selecting-a-subset-using-dropna-to-select-multiple-columns
        (5) groupby approach : https://www.youtube.com/watch?v=txMdrV1Ut64&list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS&index=11&ab_channel=CoreySchafer
        (6) extracting the count column : https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.values.html
        (7) line-chart : https://www.geeksforgeeks.org/line-chart-in-matplotlib-python/
        (8) style: https://python-charts.com/matplotlib/styles/
        (9) stretching saved line chart : https://www.geeksforgeeks.org/change-plot-size-in-matplotlib-python/
        """

        #extract 'sold_date' column
        x = dataframe['sold_date']

        #the str.extract() flags from the re module, and i can put in a pattern that i want to search for. since i want 4 digit from
        #the sold_date, i pass the following pattern.
        year = x.str.extract(r'(\d\d\d\d)')

        #creating a new column with the extracted year info
        dataframe['year'] = year

        #removes row that year is NaN
        dataframe = dataframe.dropna(subset=['year'])

        #get all unique year values
        all_year = dataframe['year'].unique()

        #sort year values in ascending order and this will be my 'x' variable
        reverse_allyear = all_year[::-1]

        #group dataframe by the year column
        year_group = dataframe.groupby(['year'])

        #approach is reffering to (5) in reference. this will count the number of values in badge column based on the year group. I chose
        #the badge column because there is only 1 value 'Sold' , and it makes it easy.
        temp_count = year_group['badge'].value_counts()

        #takes temp_count and get the values of it ((6) from reference) and this will match the order of the year. This will be my 'y' variable
        sold_count = temp_count.values

        #style of line chart
        plt.style.use("Solarize_Light2")

        fig = plt.figure()
        plt.plot(reverse_allyear, sold_count)
        plt.xlabel('Year')
        plt.ylabel('Number of properties sold')

        plt.title("Sales Trend of Properties Sold per Year")

        #adjust size of the line_chart so its not crammed
        fig.set_figwidth(10)

        #saves line_chart in figures folder
        plt.savefig('figures/sale_trend.png')

        #technically this method has no return but this message lets user know that the figure has been saved
        return f"Please find the line chart in the 'Figures' folder"


    def prop_val_distribution(self, dataframe, suburb, target_currency):

        """
        Visualizes a histogram of the property value distribution either in all suburb or specified suburb. If suburb
        does not exist, an error message will be displayed and a histogram of all suburbs will be saved.
        The histogram is basically a graph that stores a range of price in their respective bins to show the distribution.
        The code of adjusting histogram is following the default format found online.

        Parameters
        ----------
        dataframe : panda dataframe, required
            this is the same dataframe that was mentioned before

        suburb : str, required
            is the suburb that needs to be matched in the dataframe

        target_currency : str, required
            is the currency to transform the price column to target currency

        Returns
        -------
        returns a message informing user that file has been saved in folder

        References
        ---------
        Matplotlib Tutorial (Part 1): Creating and Customizing Our First Plots: https://www.youtube.com/watch?v=UO98lJQ3QGI&t=1812s&pp=ygUXY29yZXkgc2NoYWZlciBtYXRwbG9saWI%3D
        removing NaN from numpy array : https://stackoverflow.com/questions/11620914/how-do-i-remove-nan-values-from-a-numpy-array
        adjust bins of histogram : https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html
        color hist : https://matplotlib.org/stable/gallery/color/named_colors.html
        similar filtering approach from previous method in other classes
        """

        #this is for transformed prices for ALL suburbs since this method returns a numpy array  of all properties
        transformed_price = self.currency_exchange(dataframe, target_currency)

        suburb = suburb.lower()

        #to be used in conditional statements below
        all_suburb = dataframe['suburb'].unique()
        lower_all_suburb = list(map(lambda x: x.lower(), all_suburb))

        if suburb not in lower_all_suburb:

            #ensure there is no NaN values in array.
            y = transformed_price[~np.isnan(transformed_price)]

            fig = plt.figure()

            plt.hist(y, bins = 20, color = "navajowhite", ec="salmon")

            plt.xlabel('Price of Property (Millions)')
            plt.ylabel('Frequency')

            if suburb == 'all':
                plt.title(f'Price Distribution of ALL suburbs in {target_currency.upper()} Millions')

            else:

                fsuburb = suburb.title()

                print(f"Sorry, {fsuburb} suburb does not exist in our system. Please try again!")
                plt.title(f'Price Distribution of ALL suburbs in {target_currency.upper()} Millions')

            fig.set_figwidth(10)

            plt.savefig('figures/all_suburb_price_dist.png')

            return f"Please find histogram in the 'Figures' folder!"


        #for specific suburbs
        else:

            suburb = suburb.title()

            # the below follows the same filtering approach from previous methods
            filt = dataframe['suburb'] == suburb

            df_to_summarize = dataframe.loc[filt]

            #gets the transformed numpy array of the filtered dataframe
            spec_price_array = self.currency_exchange(df_to_summarize, target_currency)

            y = spec_price_array[~np.isnan(spec_price_array)]

            fig = plt.figure()

            #distributing price among 20 bins
            plt.hist(y, bins = 20, color="navajowhite", ec="salmon")

            plt.xlabel('Price of Property (Millions)')
            plt.ylabel('Frequency')
            plt.title(f'Price Distribution of {suburb} in {target_currency.upper()} Millions')

            #adjust the figure so it doesnt look crammed
            fig.set_figwidth(10)

            fsuburb = suburb.lower()

            #saves file in folder
            plt.savefig(f'figures/{fsuburb}_suburb_price_dist.png')

            return f"Please find the histogram in the 'Figures' folder"
