import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
from colorama import init, Fore, Style, Back

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
        print("\n  1. Check My Finance Report!")
        print("  2. Add new income")
        print("  3. Add new expense")
        print("  4. Exit program")

        try:
            option = int(input("\nEnter your choice (1-4):\n "))
            #print(option)

            if (option >= 1 and option <= 4):
                handle_user_option(option)
                break  # Exit the loop if valid choice
            else:
                raise ValueError("")

        except ValueError as e:
            print(f"Invalid input! {e}")
            print("Please enter a number between 1 and 4.\n")
    
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

def validate_user_choice(user_input):

    """
    Validates the user's choice.
    Raises ValueErrors if strings are provided or
    if user selects other values between 1 and 4.
    """





#User chose: 1 (Check My Finance Report! )
    #Ask User which month they want to see

    #If choice is invalid: print/raise an error
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

main()


             


    

