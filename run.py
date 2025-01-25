import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
from colorama import init, Fore, Style, Back
from datetime import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

#Create constant variables
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('my_finances')

#Make sure the API is working correctly
income = SHEET.worksheet('income')
expenses = SHEET.worksheet("expenses")

income_data = income.get_all_values()
expenses_data = expenses.get_all_values()

#pprint(income_data[1]) #output: a list of rows with string values
#pprint(expenses_data[2]) #output: a list of rows with string values

############################################# Welcome message

def welcome():

    """
    Displays a welcome message with color
    """

    init()  # Initialize colorama
    welcome_message = f"""
    \n{Fore.GREEN + Style.BRIGHT}============== WELCOME TO MyFinances APP! =============={Style.RESET_ALL}\n
    This expense tracker will help you monitor your income and expenses
    to understand your spending habits!
    
    Ready to start? Let's go! 🚀\n
{Fore.GREEN + Style.BRIGHT}========================================================{Style.RESET_ALL}
    """
    
    print(welcome_message)

#welcome()

########################################## Ask user to chooce betweeen options

def get_main_user_choice():

    """
    Gets the user's choice from the menu options.
    """
    while True:
        print(Fore.BLUE + "Please select an option:" + Style.RESET_ALL)
        print("\n  1. Check My Monthly Finance Report!")
        print("  2. Add new income")
        print("  3. Add new expense")
        print("  4. Exit program")

        try:
            option = int(input("\nEnter your choice (1-4):\n "))
            #print(option)

        #Validate the data
            validate_user_choice(option)
        #call the handle option function
            handle_user_option(option)
        # Exit the loop if valid choice
            break  

        except ValueError as e:
            print(f"{e}\n")
    
    return(option)

#get_main_user_choice()

############################################# Menu options

def handle_user_option(option):
    if option == 1:
        # return show_finance_report()
        print("show_finance_report")
    elif option == 2:
        # return add_new_income()
        print("add_new_income")
    elif option == 3:
        # return add_new_expense()
        print("add new expense")
    elif option == 4:
        # return exit()
        print("Exit program")

############################################# Raise ValueError

def validate_user_choice(user_choice):

    """
    Validates the user's choice.
    Raises ValueErrors if strings are provided or
    if user selects other values between 1 and 4.
    """
    if not 1 <= user_choice <= 4:
        raise ValueError(Fore.LIGHTRED_EX + "Invalid choice! Please enter a number between 1 and 4." + Style.RESET_ALL)


############################################# User chose: 1 (Check My Finance Report! )

def show_monthly_finance_report():
    """
    Monthly finance report
    """
    print("Monthly finance report")
    get_month_input()

            ########### Get month input from User ################

def get_month_input():
    """
    Prompts the user to enter a month name and validates the input.
    Returns the entered month name as a string, or an error if the input is invalid.
    """

    #validate the User choice:
    while True:
        #Ask User which month they want to see
        user_month = input(Fore.BLUE + "\nPlease enter the month name (e.g., january, february):\n " + Style.RESET_ALL).lower()

        try:
            datetime.strptime(user_month, "%B")
            month = user_month.title() 
            print(f"Month was selected: {month}")
            #return(month) #return the month as a string, and breaks the loop

        #If choice is invalid: print/raise an error
        except ValueError as error:
            print(Fore.LIGHTRED_EX + " Invalid month name!" + Style.RESET_ALL)
            continue #important to break the loop and jump back to the beginning of the while loop!

    
    #If choice is valid: check if the month has data:

        #No data:
            #print(there is no data for the month yet), only for ABC
            #Ask user: add new income?, add new expense? or Check expenses report for ABC?
        
        # Has data: 
            #Print: calculating your general finances in ABC:
            # ✅ Your total income in ABC was:
            # ✅ Your total expenses in ABC was:

            #Print calculating your cash balance in ABC:
            #If Positive: 🤘🏽😎 Congratulations! in ABC your cash balance is positive : ➕ amount
            #If negative: ⚠️🚨Attention!⚠️🚨 in ABC your cash balance is negative:  ➖ amount

            #Ask user: do they want to see the expenses details?(y/n)
            #If yes: 
                #Print (Your expenses details for ABC are ...)
                #Show expenses per category.
                #Show max expense category and amount
                #Show which categories have to be payed at the first day of each month (2025-01-01)
                #Ask user what they want to do next?: 
                    #add new income?, add new expense? or exit?
            
            #If no: add new income?, add new expense? or exit?

#User chose: 2 (Add new income?)
    #Request data from the user: source, amount, month

    #If choice is invalid: print/raise an error
    #If choice is valid:
        #Parse data into correct format for worksheet
        #Update income spreadsheet
        #Print data to terminal

#User chose: 3 (Add new expense?)
    #Request data from the user: source, amount, month

    #If choice is invalid: print/raise an error
    #If choice is valid:
        #Parse data into correct format for worksheet
        #Update expenses spreadsheet
        #Print data to terminal

#User chose: 4 (Exit)
    #Print (Goodbye and "See you next time! Your finances are in good hands.")

#function to call all functions
def main():
    welcome()
    get_main_user_choice()
    show_monthly_finance_report()

main()


             


    

