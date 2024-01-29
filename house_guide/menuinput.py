class MenuInput:

    """
    A class where stores all the print & general input statements to be used in main.py
    ...

    Attributes
    ----------
    none

    """

    #intro to program
    def intro(self):
        print("🏠Automation Program for Property File🏡\n")
        print("You will need to input your preferred currency. Here are all the available exchange rate:\n")


    #list of functionality print statements
    def functions(self):

        print("1. Show All Suburbs")
        print("2. Get Property Summary")
        print("3. Get Average Land Size of Property")
        print("4. Get Histogram of Property Value Distribution")
        print("5. Get Line Chart of Sales Trend")
        print("6. Locate Properties Based on Price")
        print("7. Reset Exchange Rate")
        print("8. Exit")


    #method that stores users preferred currency
    def select_currency(self):

        print("1. AUD  ")
        print("2. USD ")
        print("3. INR ")
        print("4. CNY ")
        print("5. JPY ")
        print("6. HKD ")
        print("7. KRW ")
        print("8. GBP ")
        print("9. EUR ")
        print("10. SGD\n")

        return input("Please select your preferred currency in the following format 💱💰 --> USD:\n").upper()


    # method that stores users option
    def pick_option(self):

        return input('Please input the corresponding function based on its number: ')
