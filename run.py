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

#WELCOME MESSAGE
def welcome():
    """
    Displays a welcome message with color.
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

#GET USER CHOICE
def get_main_user_choice():
    """
    Gets the user's choice from the menu options.
    """
    while True:
        print(Fore.BLUE + "Please select an option:" + Style.RESET_ALL)
        print("\n  1. Check MONTHLY Finance Report!")
        print("  2. Check ALL income and expenses")
        print("  3. Add new income")
        print("  4. Add new expense")
        print("  5. Exit program")

        try:
            option = int(input("\nEnter your choice (1-4):\n "))

        #Validate the data
            validate_user_choice(option)
        #return the handle_user_option function
            return handle_user_option(option) #return breaks the loop

        except ValueError as error:
            print(Fore.LIGHTRED_EX + f"{error}\n" + Style.RESET_ALL)
    
#VALIDATE USER CHOICE (for get_main_user_choice)
def validate_user_choice(user_choice):
    """
    Validates the user's choice.
    """
    if not 1 <= user_choice <= 4:
        raise ValueError(Fore.LIGHTRED_EX + "Invalid choice! Please enter a number between 1 and 4." + Style.RESET_ALL)

#HANDLE THE USER SELECTION (for get_main_user_choice)
def handle_user_option(option):
    """
    Handle user option.
    """
    if option == 1:
        return generate_monthly_finance_report()
        #rint("show_finance_report")
    elif option == 2:
        # return display_worksheet():
        print("Check my income and expense")
    elif option == 3:
        # return add_new_income()
        print("add_new_income")
    elif option == 4:
        # return add_new_expense()
        print("add new expense")
    elif option == 5:
        # return exit()
        print("Exit program")

# IF USER OPTION == 1
class FinanceManager: 
    #MAKE THE WORKSHEETS ACCESSIBLE FOR THE CLASS METHODS
    def __init__(self):
        self.income_worksheet = SHEET.worksheet("income")
        self.expenses_worksheet = SHEET.worksheet("income")

    #GET ALL DATA FROM A WORKSHEET
    def get_worksheet_data(worksheet):
        '''
        Gets all data from a worksheet
        '''
        worksheet = SHEET.worksheet(worksheet)
        all_values = worksheet.get_all_values()
        return all_values
    
    #GET MONTH SELECTED BY USER AND VALIDATES IT
    def get_and_validate_month_input():
        """
        Prompts the user to enter a month name and validates the input.
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

    def generate_monthly_finance_report():
        """
        Monthly finance report
        RETURNS: gets the Month input from User,

        """
        print("")
        print(Fore.GREEN + Style.BRIGHT+ "\n  ✨✨✨✨  MY MONTHLY FINANCE REPORT  ✨✨✨✨" + Style.RESET_ALL)
        
        #User gives the month
        month = get_and_validate_month_input()

        #If choice {month} is valid: check if {month} has data:
        income_worksheet = get_worksheet_data("income")
        expenses_worksheet = get_worksheet_data("expenses")

        # Check if data exists in income or expense worksheet
        income_month_data_available = month_has_data(income_worksheet, month)
        expense_month_data_available = month_has_data(expenses_worksheet, month)

        if income_month_data_available or expense_month_data_available:
            print(Fore.GREEN + Style.BRIGHT + f"\nCalculating your {month} income and expenses...\n" + Style.RESET_ALL)
            
            total_month_income = calculate_total_amount(income_worksheet, month, 2)
            total_month_expenses = calculate_total_amount(expenses_worksheet, month, 4)

            print(f"✅ TOTAL INCOME: EUR{total_month_income: .2f}")
            print(f"✅ TOTAL EXPENSES: EUR{total_month_expenses: .2f}\n")

            #Calculating cash balance
            print(Fore.GREEN + Style.BRIGHT + f"Calculating Your {month} cash balance...\n" + Style.RESET_ALL)
            cash_balance = total_month_income - total_month_expenses

            if cash_balance >= 0:
                print(f"🎉🎉 Congratulations! Positive cash balance!: EUR{cash_balance: .2f}\n")
            else:
                print(Fore.LIGHTRED_EX + f"🚨🚨 Attention! Negative cash balance!: EUR{cash_balance: .2f}\n" + Style.RESET_ALL)
            
            #return show_expenses_details()
        else:
            # No data for the month
            print(f"There is no data for {month} yet.")
            # Ask user: add new income?, add new expense? or Check expenses report for ABC?


        
    
    
    #3) ************ Checks if data exists for the selected month in a worksheet.
    def month_has_data(worksheet_data, month):
        """
        Checks and returns true if data exists for a specific month in a worksheet.
        """

        for row in worksheet_data:
            if row[0].lower() == month.lower():
            return True
        return False

    #4) ************* If month has data, calculates total amount in selected month: 
    def calculate_total_amount(worksheet_data, month, amount_col_index):
        """
        Calculates and returns the total amount for the given month and worksheet
        """

        total_amount = 0
        for row in worksheet_data:             # interates through each row in the worksheet
            if row[0].lower() == month.lower(): #first value after the month header
                total_amount += float(row[amount_col_index])
        return total_amount

#CALL WELCOME AND USER CHOICE functions
def main():
    welcome()
    get_main_user_choice()

main()

#5) ************* If user wants, show expenses details
# def show_expenses_details():

#     try:
#         show_details = validate_expense_details()
        
#         if show_details:
#             print("Your expenses details for ABC are ...")
#             # 7) Show expenses per category -->
#             return calculate_expenses_by_category()

#             # 8) Show max expense category and amount
#             #return max_expense_by_category()

#             # 9) Show which categories have to be payed at the first day of each month (2025-01-01)
#             #return find_first_day_payments():

#             #And Ask user what they want to do next?: 
#         elif show_details == False:
#             print("#add new income?, add new expense? or exit?")
#     except ValueError as error:
#         print(f"{error}")

# #6) ************* Confirms the users choice to see or not their detailed expense information.
# def validate_expense_details():
#     """
#      Confirms the users choice to see or not their detailed expense information.
#     RETURNS -> True if the user says yes, False otherwise.
#     Raises: ValueError: If the user input is invalid (not 'y' or 'n').
#     """
#     while True:
#         #Ask user: do they want to see the expenses details?(y/n)
#         see_details = input(f"{Fore.BLUE} Do you want to see your expenses details?(y/n) {Style.RESET_ALL}: ").lower()
         
#         if see_details == "y":
#             return True
#         elif see_details == "n":
#             return False
#         else:
#             raise ValueError(Fore.LIGHTRED_EX + "Invalid input! Please enter 'y' or 'n'" + Style.RESET_ALL) 

# #7) ****** Show expenses per category.
# def calculate_expenses_by_category(month):
#     """
#     Calculate expenses per category in a given month
#     """
#     expenses_by_category = {} #create a dictionary
#     for row in expenses_by_category:
#         if row[0].lower() == month.lower():
#             category = row[2]
#             print(category)
            

# #8) ****** Show max expense category and amount
# def max_expense_by_category():
#     pass

# #9) ****** Show which categories have to be payed at the first day of each month (2025-01-01)
# def find_first_day_payments():
#     pass



#############################################
#####################

#User chose: 2 (Add new income?)
    #Request data from the user: source, amount, month

    #If choice is invalid: print/raise an error
    #If choice is valid:
        #Parse data into correct format for worksheet
        #Update income spreadsheet
        #Print data to terminal

#****** Give User their Data  *****
# def display_income_worksheet():
#     '''
#     get income worksheet data
#     '''
#     print(Fore.GREEN + Style.BRIGHT + "\nGetting your income data...\n" + Style.RESET_ALL) #give user some feedback in the terminal
#     income_worksheet = SHEET.worksheet("income")
#     #print(income_worksheet) #<Worksheet 'income' id:1680754323>

#     all_income_values = income_worksheet.get_all_values()
#     #print(all_income_values)
#     #print(all_income_values[1]) #access the first row, after the headers

#     # Get header row
#     header_row = all_income_values[0] #output= list of string values
#     #print(header_row)

#     #Get data rows
#     data_rows = all_income_values[1:]
#     #print(data_rows)

#     # Print header
#     print(" | ".join(header_row))   # join makes a single string with the headers separated by pipes.
#     print("-" * (len(header_row) * 9))  # separator line

#     #Display All income data
#     for row in data_rows:  # Do not take the header row
#         print(" | ".join(row))
#         print("-" * (len(row) * 9))

# def display_expenses_worksheet():
#     '''
#     get income worksheet data
#     '''
#     print(Fore.GREEN + Style.BRIGHT + f"\nGetting your expenses data ...\n" + Style.RESET_ALL) #give user some feedback in the terminal
#     expenses_worksheet = SHEET.worksheet("expenses") 

#     all_expenses_values = expenses_worksheet.get_all_values()
#     #print(all_expenses_values)
#     #print(all_expenses_values[1]) #access the first row, after the headers

#     # Get header row
#     header_row = all_expenses_values[0] #output= list of string values
#     #print(header_row)

#     #Get data rows
#     data_rows = all_expenses_values[1:]
#     #print(data_rows)

#     # Print header
#     print(" | ".join(header_row))   # join makes a single string with the headers separated by pipes.
#     print("-" * (len(header_row) * 9))  # separator line

#     #Display All income data
#     for row in data_rows:  # Do not take the header row
#         print(" | ".join(row))
#         print("-" * (len(row) * 9))

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




             


    

