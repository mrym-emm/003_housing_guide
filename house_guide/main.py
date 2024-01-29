from menuinput import MenuInput
from data_visualizer import DataVisualizer

#Test code is at end of file


def main():

    #had to add this for program when user chooses to reset
    program_running = True

    #code will run since program_running is True
    while program_running:

        file_path = 'data/property_information.csv'

        #initiate MenuInput object, to call methods
        program = MenuInput()

        program.intro()

        #to ensure user's input is in list of currency
        list_currency = ["AUD", "USD", "INR", "CNY", "JPY", "HKD", "KRW", "GBP", "EUR", "SGD"]


        while True:

            #asks user for their preferred currency
            exchange_rate = program.select_currency()

            if exchange_rate in list_currency:
                break
            else:
                print("The currency you've inputted is not available. Please try again!\n")


        #inititate DataVisualizer object
        data1 = DataVisualizer(file_path)

        #load dataframe
        int_dataframe = data1.extract_property_info(file_path)

        #get dataframe of transformed prices. Will use this for the rest of the program
        dataframe = data1.transformed_price_dataframe(int_dataframe, exchange_rate)

        #get all unique suburb in file
        display_suburbs = dataframe['suburb'].unique()

        #display program's functionality
        program.functions()


        while True:

            option = int(program.pick_option())

            if option == 1:


                print("\nHere are ALL suburbs available in the file:\n")

                print(display_suburbs)

                print(f"\nThere are {len(display_suburbs)} suburbs")


            elif option == 2:

                while True:

                    target_suburb = input("Please input your selected suburb. Enter 'all' for ALL suburbs:\n").title()

                    if target_suburb in display_suburbs or target_suburb.lower() == 'all':
                        break
                    else:
                        print(f"Sorry. {target_suburb} not found. Please try another suburb ☹\n")


                function = data1.suburb_summary(dataframe, target_suburb)

                print(f"{function}")

            elif option == 3:

                while True:

                    target_suburb = input("Please input your selected suburb. Enter 'all' for ALL suburbs:\n").title()

                    if target_suburb in display_suburbs or target_suburb == 'All':
                        break

                    else:
                        print(f"Sorry. {target_suburb} not found. Please try another suburb ☹\n")


                function = data1.avg_land_size(dataframe, target_suburb)

                print(f"{function}")

            elif option == 4:


                target_suburb = input("Please input your selected suburb. Enter 'all' for ALL suburbs:\n").title()

                function = data1.prop_val_distribution(dataframe, target_suburb, exchange_rate)

                #to display print statement in method
                print(f"{function}")

            elif option == 5:

                function = data1.sales_trend(dataframe)
                print(function)


            elif option == 6:

                while True:

                    target_suburb = input('Please input your selected suburb:\n').title()

                    if target_suburb in display_suburbs:
                        break

                    else:
                        print(f"Sorry. {target_suburb} not found. Please try another suburb ☹\n")


                filt = dataframe['suburb'] == target_suburb.title()
                df_to_summarize = dataframe.loc[filt]

                print(f"Below are are all the prices available in {target_suburb.title()}")

                display_unordered_prices = df_to_summarize['conv_price']

                print(display_unordered_prices)


                while True:
                    try:
                        target_price = float(input('Please input your target price🎯:\n'))
                        break

                    except:
                        print("Please only input digits!")


                rows_to_display = data1.get_rows_of_specific_price(target_price, dataframe, target_suburb)

                print(rows_to_display)


            elif option == 7:

                #if users want to reset currency
                print("---Resetting Currency---")
                break


            elif option == 8:

                print("---Program Shutting Down---")
                program_running = False
                break

            print("\n")

            #shows the functionality everytime an options execures
            program.functions()



if __name__ == "__main__":
    main()


#Test Code

# file_path = 'data/property_information.csv'

# test_df = DataVisualizer(file_path)

#program will convert this to uppercase later
# exchange_rate = 'eur'

# -------------------------------------------------------------------------------

#3.2. Extracting Property Information

# dataframe = test_df.extract_property_info(file_path)

# print(dataframe)

# output:

#                id badge   suburb  ... auction_date  available_date  sold_date
# 0       141922512  Sold  Clayton  ...          NaN             NaN   3/4/2023
# 1       141599568  Sold  Clayton  ...          NaN             NaN   3/4/2023
# 2       141574624  Sold  Clayton  ...          NaN             NaN   1/4/2023
# 3       141840188  Sold  Clayton  ...          NaN             NaN  29/3/2023
# 4       141462600  Sold  Clayton  ...          NaN             NaN  29/3/2023
# ...           ...   ...      ...  ...          ...             ...        ...
# 118709  106245306  Sold  Burwood  ...          NaN             NaN  14/2/2010
# 118710  106246497  Sold  Burwood  ...          NaN             NaN  13/2/2010
# 118712  106273193  Sold  Burwood  ...          NaN             NaN   3/2/2010
# 118713    2704784  Sold  Burwood  ...          NaN             NaN   3/2/2010
# 118715  106242388  Sold  Burwood  ...          NaN             NaN  27/1/2010
#
# [104833 rows x 20 columns]

#output is a pandas dataframe that is removes row with NaN in price

# -------------------------------------------------------------------------------

#3.3. Currency Exchange

# print(test_df.currency_exchange(dataframe, exchange_rate))

#the first, second, third price value in the default file in AUD is
#[965000, 405000, 881000....]

#since the exchange_rate of EUR is 0.60 then the numpy array returned is correct

#output:
#[579000. 243000. 528600. ... 454800. 402000. 312480.]

# -------------------------------------------------------------------------------

#3.4. Suburb Property Summary

#program will transform the suburb into title case to match the ones in the file
# suburb1 = 'boX hiLL'

# print(test_df.suburb_summary(dataframe, suburb1))

#output:

#     📜Below is a summary for properties in Box Hill📜
#
#       bedrooms  bathrooms  parking_spaces
# mean      2.51       1.49            1.35
# std       1.26       0.67            1.05
# 50%       2.00       1.00            1.00
# min       0.00       1.00            0.00
# max      12.00       6.00           18.00

#all suburbs
# suburb2 = 'alL'

# print(test_df.suburb_summary(dataframe, suburb2))

#output:

#      📜Below is a summary for ALL suburbs📜
#
#       bedrooms  bathrooms  parking_spaces
# mean      3.24       1.76            1.82
# std       1.01       0.75            2.70
# 50%       3.00       2.00            2.00
# min       0.00       0.00            0.00
# max      30.00      20.00          819.00

#non-exisiting suburbs
# suburb3 = 'alLjsdb'

# print(test_df.suburb_summary(dataframe, suburb3))

# output:Per specification, if suburb does not exist, summary of all will be displayed along with an error message

#      📜Below is a summary for ALL suburbs📜
#
#       bedrooms  bathrooms  parking_spaces
# mean      3.24       1.76            1.82
# std       1.01       0.75            2.70
# 50%       3.00       2.00            2.00
# min       0.00       0.00            0.00
# max      30.00      20.00          819.00
# Sorry. Alljsdb not found. Please try another suburb ☹

# -------------------------------------------------------------------------------

# 3.5. Average Land Size

#disclaimer: the dataframe used is the one from task 3.2 and that dataframe removes rows with NaN in price
#land_size is in hectars and output will be in m2

# print(test_df.avg_land_size(dataframe, suburb1))

# output: The average land size in Box Hill is 5852680.73 m2

# print(test_df.avg_land_size(dataframe, suburb2))

# output: The average land size for ALL suburb is 6218179.96 m2

# print(test_df.avg_land_size(dataframe, suburb3))

#output (error message): Sorry. There are no properties in Alljsdb. Please try another suburb ☹

# -------------------------------------------------------------------------------

# 3.6. Property Value Distribution

#if the same suburb is passed but different exchange rate, it will overrride the file
#if suburb does not exist, histogram of all suburbs will be saved

# print(test_df.prop_val_distribution(dataframe, suburb1,exchange_rate))

#output (will display message of file being saved in 'figures' folder):
#Please find the histogram in the 'Figures' folder
#file name:box hill_suburb_price_dist.png

# print(test_df.prop_val_distribution(dataframe, suburb3 ,exchange_rate))

#output (will display message of file being saved in folder):
#Please find the histogram in the 'Figures' folder
#file name:all_suburb_price_dist.png

# -------------------------------------------------------------------------------

# 3.7 Sales Trend

# print(test_df.sales_trend(dataframe))

#output (will display message of file being saved in folder):
#Please find the line chart in the 'Figures' folder
#file name:sale_trend.png

# -------------------------------------------------------------------------------

# 3.8. Identifying a Property of a Specific Price in a Suburb

#This method uses a dataframe which has the conv_price. This dataframe is returned via the method
#transformed_price_dataframe.

# dataframe1 = test_df.transformed_price_dataframe(dataframe, exchange_rate)

#test with target_price in file
# target_price1 = 750000

# target_suburb = suburb1

# print(test_df.locate_price(target_price1, dataframe1, target_suburb))
#output : True

#test with target_price not in file
# target_price2 = 7500003764

# target_suburb = suburb1

# print(test_df.locate_price(target_price2, dataframe1, target_suburb))
#output : False

# -------------------------------------------------------------------------------

#Additional methods (not in brief)

#3.9 transformed_price_dataframe

#returns a dataframe with new column of transformed price called conv_price at the end of the dataframe

# dataframe1 = test_df.transformed_price_dataframe(dataframe, exchange_rate)

# print(dataframe1)

# output:
#
#                id badge   suburb  ... available_date  sold_date conv_price
# 0       141922512  Sold  Clayton  ...            NaN   3/4/2023   579000.0
# 1       141599568  Sold  Clayton  ...            NaN   3/4/2023   243000.0
# 2       141574624  Sold  Clayton  ...            NaN   1/4/2023   528600.0
# 3       141840188  Sold  Clayton  ...            NaN  29/3/2023   642000.0
# 4       141462600  Sold  Clayton  ...            NaN  29/3/2023   300000.0
# ...           ...   ...      ...  ...            ...        ...        ...
# 118709  106245306  Sold  Burwood  ...            NaN  14/2/2010   336000.0
# 118710  106246497  Sold  Burwood  ...            NaN  13/2/2010   399000.0
# 118712  106273193  Sold  Burwood  ...            NaN   3/2/2010   454800.0
# 118713    2704784  Sold  Burwood  ...            NaN   3/2/2010   402000.0
# 118715  106242388  Sold  Burwood  ...            NaN  27/1/2010   312480.0
#
# [104833 rows x 21 columns]

# -------------------------------------------------------------------------------

#4.0 get_rows_of_specific_price

#return dataframe that matches target_price

#test with target_price in file
# target_price1 = 750000

# print(test_df.get_rows_of_specific_price(target_price1, dataframe1, suburb1))

# output:
#                id    suburb  bedrooms  bathrooms  parking_spaces  conv_price
# 112818  141579432  Box Hill       4.0        3.0             2.0    750000.0
# 113273  132610106  Box Hill       2.0        1.0             1.0    750000.0
# 113713  114810791  Box Hill       5.0        3.0             1.0    750000.0

#test with target_price in file
# target_price2 = 750000345

# print(test_df.get_rows_of_specific_price(target_price2, dataframe1, suburb1))
#outputs:
# No properties to display matching that price
