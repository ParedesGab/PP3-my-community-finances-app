import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
from colorama import init, Fore, Style, Back
from datetime import datetime
#import pandas as pd

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
# income = SHEET.worksheet('income')
# expenses = SHEET.worksheet("expenses")

# income_data = income.get_all_values()
# expenses_data = expenses.get_all_values()

# #pprint(income_data[1]) #output: a list of rows with string values
# #pprint(expenses_data[2]) #output: a list of rows with string values

############################################# Welcome message

def welcome():

    """
    Displays a welcome message with color
    RETURNS: Printed welcome message
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
    RETURNS: The option (1-4) chosen by the user (if valid)
    RETURNS: A ValueError (if invalid)
    """
    while True:
        print(Fore.BLUE + "Please select an option:" + Style.RESET_ALL)
        print("\n  1. Check My Monthly Finance Report!")
        print("  2. Check my income and expenses")
        print("  3. Add new income")
        print("  4. Add new expense")
        print("  5. Exit program")

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
            print(Fore.LIGHTRED_EX + f"{e}\n" + Style.RESET_ALL)
    
    return(option)

#get_main_user_choice()

############################################# Menu options

def handle_user_option(option):

    """
    Handle user option
    RETURNS: The function of each option
    """
    if option == 1:
        return monthly_finance_report()
        #rint("show_finance_report")
    elif option == 2:
        # return display_worksheet():
        print("Check my income and expense")
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
    RAISES:  ValueErrors if strings are provided or if user selects
    other values between 1 and 4.
    """
    if not 1 <= user_choice <= 4:
        raise ValueError(Fore.LIGHTRED_EX + "Invalid choice! Please enter a number between 1 and 4." + Style.RESET_ALL)

############################################# User chose: 1 (Check My Finance Report! )

def monthly_finance_report():
    """
    Monthly finance report
    RETURNS: gets the Month input from User,

    """
    print("")
    print(Fore.GREEN + Style.BRIGHT+ "\n✨ MY MONTHLY FINANCE REPORT ✨" + Style.RESET_ALL)
    
    #User gives the month
    month = get_month_input()

    #If choice {month} is valid: check if {month} has data:
    income_worksheet = get_worksheet_data("income")
    expenses_worksheet = get_worksheet_data("expenses")

    # Check if data exists in income or expense worksheet
    income_month_data_available = month_has_data(income_worksheet, month)
    expense_month_data_available = month_has_data(expenses_worksheet, month)

    if income_month_data_available or expense_month_data_available:
    # Display report (implementation needed)
        print(f"This is your report for {month}")
    else:
        # No data for the month
        print(f"There is no data for {month} yet.")
        # Ask user: add new income?, add new expense? or Check expenses report for ABC?

#****** Get month input from User *****

def get_month_input():
    """
    Prompts the user to enter a month name and validates the input.
    RETURNS: Month (if valid)
    RETURNS: ValueError (if invalid)
    """

    #validate the User choice:
    while True:
        #Ask User which month they want to see
        user_month = input(Fore.BLUE + "\nPlease enter the month name (e.g., january, february):\n " + Style.RESET_ALL).lower()

        try:
            datetime.strptime(user_month, "%B")
            month = user_month.title() 
            #print(f"Month was selected: {month}")
            return(month) #return the month as a string, and breaks the loop

        #If choice is invalid: print/raise an error
        except ValueError as error:
            print(Fore.LIGHTRED_EX + " Invalid month name!" + Style.RESET_ALL)
            continue #important to break the loop and jump back to the beginning of the while loop!
  
#****** Get DATA from the worksheets *****

def get_worksheet_data(worksheet):
    '''
    get worksheet data to be used in calculations
    '''
    worksheet = SHEET.worksheet(worksheet)
    all_values = worksheet.get_all_values()
    
    return(all_values)

#************* Checks if data exists for a specific month in a worksheet.
def month_has_data(worksheet_data, month):
  """
  Checks if data exists for a specific month in a worksheet.
  RETURNS. True if data exists for the month, False otherwise.
  """

  for row in worksheet_data:
    if row[0].lower() == month.lower():
      return True
  return False

#function to call all functions
def main():
    welcome()
    get_main_user_choice()
   #show_monthly_finance_report()

main()
       
    

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

#****** Give User their Data  *****
def display_income_worksheet():
    '''
    get income worksheet data
    '''
    print(Fore.GREEN + Style.BRIGHT + "\nGetting your income data...\n" + Style.RESET_ALL) #give user some feedback in the terminal
    income_worksheet = SHEET.worksheet("income")
    #print(income_worksheet) #<Worksheet 'income' id:1680754323>

    all_income_values = income_worksheet.get_all_values()
    #print(all_income_values)
    #print(all_income_values[1]) #access the first row, after the headers

    # Get header row
    header_row = all_income_values[0] #output= list of string values
    #print(header_row)

    #Get data rows
    data_rows = all_income_values[1:]
    #print(data_rows)

    # Print header
    print(" | ".join(header_row))   # join makes a single string with the headers separated by pipes.
    print("-" * (len(header_row) * 9))  # separator line

    #Display All income data
    for row in data_rows:  # Do not take the header row
        print(" | ".join(row))
        print("-" * (len(row) * 9))

def display_expenses_worksheet():
    '''
    get income worksheet data
    '''
    print(Fore.GREEN + Style.BRIGHT + f"\nGetting your expenses data ...\n" + Style.RESET_ALL) #give user some feedback in the terminal
    expenses_worksheet = SHEET.worksheet("expenses") 

    all_expenses_values = expenses_worksheet.get_all_values()
    #print(all_expenses_values)
    #print(all_expenses_values[1]) #access the first row, after the headers

    # Get header row
    header_row = all_expenses_values[0] #output= list of string values
    #print(header_row)

    #Get data rows
    data_rows = all_expenses_values[1:]
    #print(data_rows)

    # Print header
    print(" | ".join(header_row))   # join makes a single string with the headers separated by pipes.
    print("-" * (len(header_row) * 9))  # separator line

    #Display All income data
    for row in data_rows:  # Do not take the header row
        print(" | ".join(row))
        print("-" * (len(row) * 9))

#User chose: 3 (Add new income?)
    #Request data from the user: source, amount, month

    #If choice is invalid: print/raise an error
    #If choice is valid:
        #Parse data into correct format for worksheet
        #Update income spreadsheet
        #Print data to terminal

#User chose: 4 (Add new expense?)
    #Request data from the user: source, amount, month

    #If choice is invalid: print/raise an error
    #If choice is valid:
        #Parse data into correct format for worksheet
        #Update expenses spreadsheet
        #Print data to terminal

#User chose: 5 (Exit)
    #Print (Goodbye and "See you next time! Your finances are in good hands.")




             


    

