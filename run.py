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
        finance_manager = FinanceManager() 
        return finance_manager.generate_monthly_finance_report()
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

    #GET ALL DATA FROM A WORKSHEET (for generate_monthly_finance_report)
    def get_worksheet_data(self, worksheet):
        '''
        Gets all data from a worksheet
        '''
        worksheet = SHEET.worksheet(worksheet)
        all_values = worksheet.get_all_values()
        return all_values
    
    #GET MONTH SELECTED BY USER AND VALIDATES IT (for generate_monthly_finance_report)
    def get_and_validate_month_input(self):
        """
        Prompts the user to enter a month name and validates the input.
        """
        #validate the user's choice:
        while True:
            #Ask User which month they want to see
            user_month = input(Fore.BLUE + "\nPlease enter the month name (e.g., january, february):\n " + Style.RESET_ALL).lower()

            try:
                datetime.strptime(user_month, "%B")
                month = user_month.title() 
                #print(f"Month was selected: {month}")
                return month #return the month as a string, and breaks the loop

            #If choice is invalid: ValueError
            except ValueError as error:
                print(Fore.LIGHTRED_EX + " Invalid month name!" + Style.RESET_ALL)
                #continue #important to break the loop and jump back to the beginning of the while loop!
    
    #CHECK IF MONTH SELECTED HAS DATA (for generate_monthly_finance_report)
    def month_has_data(self, worksheet_data, month):
        """
        Checks if data exists for a specific month in a worksheet.
        """
        for row in worksheet_data:
            if row[0].lower() == month.lower():
                	return True
        return False

    #CALCULATE TOTAL INCOME AND TOTAL EXPENSES FOR THE GIVEN MONTH AND WORKSHEET (for generate_monthly_finance_report)
    def calculate_total_amount(self, worksheet_data, month, amount_col_index):
        """
        Calculates the total amount for the given month and worksheet.
        """
        total_amount = 0
        for row in worksheet_data:             # interates through each row in the worksheet
            if row[0].lower() == month.lower(): #first value after the month header
                try:
                    total_amount += float(row[amount_col_index])
                except ValueError as error:
                    print(f"{error} Warning: Could not convert amount in {row} to a number.")
        return total_amount
    
    # #ASKS USER IF THEY WANT TO SEE EXPENSES DETAILS AND VALIDATE CHOICE (for generate_monthly_finance_report)
    # def validate_see_expenses_details_choice(self):
    #     """
    #     Confirms the users choice to see detailed expense information.
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
    
    #CALCULATE EXPENSES BY CATEGORY (for show_monthly_expenses_details)
    def calculate_expenses_by_category(self, expenses_data, month):
        """
        Calculate expenses per category in a given month.
        """
        expenses_by_category = {} #create a dictionary
        #expenses_by_category = [] #create a list

        for row in expenses_data:    
            if row[0].lower() == month.lower():
                category = row[2]
                try:
                    amount = float(row[4])
                except ValueError:
                    print(f"Warning: Could not convert amount in row {row} to a number.")
                    continue
                if category in expenses_by_category:
                    expenses_by_category[category] += amount
                else:
                    expenses_by_category[category] = amount
        return expenses_by_category
    
    #MAX EXPENSE PER CATEGORY (for show_monthly_expenses_details)
    def max_expense_by_category(self, expenses_by_category):
        #expenses_by_category is a dictionary
        """
        Finds the category with the maximum expense
        """
        #print(Fore.GREEN + Style.BRIGHT + "🎯 HIGHEST EXPENSE:" + Style.RESET_ALL)
        max_category = max(expenses_by_category, key = expenses_by_category.get)
        #print(max_category)
        max_amount = expenses_by_category[max_category]

        return max_category, max_amount

    #Ask user what they want to do next?: 
    # elif show_details == False:
    #     print("#add new income?, add new expense? or exit?")1


    #IF USER SAYS "y": SHOW EXPENSES DETAILS (for generate_monthly_finance_report)
    def show_monthly_expenses_details(self, month):
        """
        Displays detailed expense information for a given month.
        """
        print(f"{Fore.GREEN + Style.BRIGHT}\nCalculating Your {month} detailed expense report...\n {Style.RESET_ALL}")

        #Show expenses per category
        expenses_data = self.get_worksheet_data("expenses")
        expenses_by_category = self.calculate_expenses_by_category(expenses_data, month)

        for category, amount in expenses_by_category.items():
            print(f"→ {category}: EUR {amount:.2f}\n")

        #Show max expense by category
        max_category, max_amount = self.max_expense_by_category(expenses_by_category)
        print(f"{Fore.GREEN + Style.BRIGHT}🎯 HIGHEST EXPENSE:{Style.RESET_ALL} {max_category.upper()} (EUR {max_amount:.2f})\n")
        
    #MONTHLY FINANCE REPORT
    def generate_monthly_finance_report(self):
        """
        Generates and displays the monthly finance report!
        """
        print("")
        print(Fore.GREEN + Style.BRIGHT+ "\n  ✨✨✨✨  MY MONTHLY FINANCE REPORT  ✨✨✨✨" + Style.RESET_ALL)
        
        #User inputs the month
        month = self.get_and_validate_month_input()

        #Get all data of a worksheet
        income_data = self.get_worksheet_data("income")
        expenses_data = self.get_worksheet_data("expenses")

        # Check if the month exists within the data
        income_month_data_available = self.month_has_data(income_data, month)
        expense_month_data_available = self.month_has_data(expenses_data, month)

        if income_month_data_available or expense_month_data_available:
            print(Fore.GREEN + Style.BRIGHT + f"\nCalculating your {month} income and expenses...\n" + Style.RESET_ALL)
            
            total_month_income = self.calculate_total_amount(income_data, month, 2)
            total_month_expenses = self.calculate_total_amount(expenses_data, month, 4)

            print(f"✅ TOTAL INCOME: EUR{total_month_income: .2f}")
            print(f"✅ TOTAL EXPENSES: EUR{total_month_expenses: .2f}\n")

            #Calculate cash balance
            print(Fore.GREEN + Style.BRIGHT + f"\nCalculating Your {month} cash balance...\n" + Style.RESET_ALL)
            cash_balance = total_month_income - total_month_expenses

            if cash_balance >= 0:
                print(f"🎉🎉 Congratulations! Positive cash balance!: EUR{cash_balance: .2f}\n")
            else:
                print(Fore.LIGHTRED_EX + f"🚨🚨 Attention! Negative cash balance!: EUR{cash_balance: .2f}\n" + Style.RESET_ALL)
        else:
            print(f"There is no data for {month} yet.")
            # Ask user: add new income?, add new expense? or Check expenses report for ABC?
              
        #if self.validate_see_expenses_details_choice():
        monthly_expenses_details = self.show_monthly_expenses_details(month)        

#CALL WELCOME AND USER CHOICE functions
def main():
    welcome()
    get_main_user_choice()

main()










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




             


    

