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
    elif option == 2:
        finance_manager = FinanceManager()
        print(Fore.BLUE + "\n**Income Data**" + Style.RESET_ALL)
        finance_manager.display_worksheet("income") 
        print(Fore.BLUE + "\n**Expense Data**" + Style.RESET_ALL)
        finance_manager.display_worksheet("expenses") 
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
        
        while True: 
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

                monthly_expenses_details = self.show_monthly_expenses_details(month)
                # Ask user: Check expenses report for ABC?  add new income?, add new expense? or 
            else:
                print(f"{Fore.LIGHTRED_EX}\nThere is no data for {month} yet... {Style.RESET_ALL}")
                print("\nWould you like to:")
                print("1. Enter a different month")
                #print("2. Exit program")
                choice = input("\nEnter your choice (1 or 2):\n ")
                if choice == '1':
                    continue  # Restart the loop to prompt for another month
                else:
                    break 
                # Ask user: add new income?, add new expense? or Check expenses report for ABC?
    
    # IF USER OPTION == 2  (Check my income and expense!)
    def display_worksheet(self, worksheet):
        '''
        get data from a given worksheet.
        '''
        print(f"\n{Fore.GREEN + Style.BRIGHT}Getting your {worksheet} data...\n{Style.RESET_ALL}")

        #all_income_values = income_worksheet.get_all_values()
        all_worksheet_values = self.get_worksheet_data(worksheet)

        # Get header row
        header_row = all_worksheet_values[0] #output= list of string values
        #print(header_row)

        #Get data rows
        data_rows = all_worksheet_values[1:]
        #print(data_rows)

        # Print header
        print(" | ".join(header_row))   # join makes a single string with the headers separated by pipes.
        print("-" * (len(header_row) * 9))  # separator line

        #Display All income data
        for row in data_rows:  # Do not take the header row
            print(" | ".join(row))
            print("-" * (len(row) * 9))
    
    # IF USER OPTION == 3  (Add new income)
    def add_new_income(self):
        """
        Adds a new income record to the "income" worksheet.
        """
        while True:
            try:
                #Request data from the user: source, amount, month
                source = input(Fore.BLUE + "Enter income source: " + Style.RESET_ALL)
                amount = float(input(Fore.BLUE + "Enter income amount: " + Style.RESET_ALL)) 
                month = self.get_and_validate_month_input() 
        
                #If choice is invalid: print/raise an error
    #If choice is valid:
        #Parse data into correct format for worksheet
        #Update income spreadsheet
        #Print data to terminal

# '''
#     Receives a list of integers to be inserted into a worksheet.
#     Update the relevant worksheet with the data provided 
#     '''
#     print(f"Updating {worksheet} worksheet...") 
#     worksheet_to_update = SHEET.worksheet(worksheet) 
#     worksheet_to_update.append_row(data)
#     print(f"{worksheet} worksheet updated successfully.\n")

#CALL WELCOME AND USER CHOICE functions
def main():
    welcome()
    get_main_user_choice()

main()



#User chose: 4 (Add new expense?)
    #Request data from the user: source, amount, month

    #If choice is invalid: print/raise an error
    #If choice is valid:
        #Parse data into correct format for worksheet
        #Update expenses spreadsheet
        #Print data to terminal

#User chose: 5 (Exit)
    #Print (Goodbye and "See you next time! Your finances are in good hands.")




             


    

