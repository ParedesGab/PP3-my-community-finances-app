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
        print("\n  1. Check My Monthly Finance Report!")
        print("  2. Display All My Income and Expenses.")
        print("  3. Add New Income.")
        print("  4. Add New Expense.")
        print("  5. Exit Program.")

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
    if not 1 <= user_choice <= 5:
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

        print(Fore.GREEN + Style.BRIGHT + "\n****************************************************" + Style.RESET_ALL)
        print(Fore.BLUE + "\nWhat would like to do next?" + Style.RESET_ALL)
        return get_main_user_choice()

    elif option == 3:
        finance_manager = FinanceManager() 
        finance_manager.add_new_income_to_income_worksheet()

    elif option == 4:
        finance_manager = FinanceManager() 
        finance_manager.add_new_expense_to_expense_worksheet()

    elif option == 5:
        print(Fore.GREEN + Style.BRIGHT + "✨ Your finances are in good hands ✨ Goodbye and See you next time!\n" + Style.RESET_ALL)
        exit()

class FinanceManager: 
    #MAKE THE WORKSHEETS ACCESSIBLE FOR THE CLASS METHODS
    def __init__(self):
        self.income_worksheet = SHEET.worksheet("income")
        self.expenses_worksheet = SHEET.worksheet("expenses")

    #GET ALL DATA FROM A WORKSHEET (for generate_monthly_finance_report)
    def get_worksheet_data(self, worksheet):
        '''
        Gets all data from a worksheet
        '''
        worksheet = SHEET.worksheet(worksheet)
        all_values = worksheet.get_all_values()
        return all_values

    # IF USER OPTION == 1
    #GET MONTH SELECTED BY USER AND VALIDATES IT (for generate_monthly_finance_report)
    def get_and_validate_month_input(self):
        """
        Prompts the user to enter a month name and validates the input.
        """
        #validate the user's choice:
        while True:
            #Ask User which month they want to see
            user_month = input(Fore.BLUE + "\nPlease enter the month name (e.g., january):\n " + Style.RESET_ALL).lower()

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
                print(Fore.GREEN + Style.BRIGHT + "\n****************************************************" + Style.RESET_ALL)
                print(Fore.BLUE + "\nWhat would like to do next?" + Style.RESET_ALL)
                return get_main_user_choice()

            else:
                print(f"{Fore.LIGHTRED_EX}\nThere is no data for {month} yet... {Style.RESET_ALL}")
                # Ask user: add new income?, add new expense? or Check expenses report for ABC?
                print(Fore.BLUE + "\nWhat would like to do next?" + Style.RESET_ALL)
                return get_main_user_choice()
    
    # IF USER OPTION == 2  (Check my income and expense!)
    def display_worksheet(self, worksheet):
        '''
        get data from a given worksheet.
        '''
        print(f"\n{Fore.GREEN + Style.BRIGHT}Getting Your {worksheet.capitalize()} data...\n{Style.RESET_ALL}")

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

        #Display All income or expenses data
        for row in data_rows:  # Do not take the header row
            print(" | ".join(row))
            print("-" * (len(row) * 9))
    
    # IF USER OPTION == 3 (Add new expenses)
    def add_new_income_to_income_worksheet(self):
        """
        Adds a new income record to the "income" worksheet.
        """
        print(Fore.GREEN + Style.BRIGHT + "\n TO ADD A NEW INCOME:" + Style.RESET_ALL)

        month = self.get_and_validate_month_input()
        source = input(Fore.BLUE + "Enter income source:\n " + Style.RESET_ALL)
        while True:
            try:
                amount = float(input(Fore.BLUE + "Enter income amount:\n " + Style.RESET_ALL))

                new_income_row = [month, source, amount]

                self.income_worksheet.append_row(new_income_row)

                print(f"\n{Fore.GREEN + Style.BRIGHT}New income for {month} from {source} (EUR {amount:.2f}) added successfully!{Style.RESET_ALL}")
                self.display_worksheet("income")

                print(Fore.GREEN + Style.BRIGHT + "\n****************************************************" + Style.RESET_ALL)

                print(Fore.BLUE + "\nWhat would like to do next?" + Style.RESET_ALL)
                return get_main_user_choice()

            except ValueError as error:
                print(Fore.LIGHTRED_EX + f"Invalid input: {error}. Please enter a valid amount.\n" + Style.RESET_ALL)

    # IF USER OPTION == 4 (Add new expenses)
    def add_new_expense_to_expense_worksheet(self):
        """
        Adds a new expense record to the "expenses" worksheet, ensuring consistency between month and date.
        """
        while True:
            try:
                month = self.get_and_validate_month_input()
                # Get the current year

                date = input(Fore.BLUE + "Enter expense date (YYYY-MM-DD): " + Style.RESET_ALL)
                # Validate date format and consistency with month
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                if date_obj.month != datetime.strptime(month, "%B").month:
                    raise ValueError(f"Date '{date}' does not match the entered month '{month}'")

                category = input(Fore.BLUE + "Enter expense category: " + Style.RESET_ALL)
                description = input(Fore.BLUE + "Enter expense description: " + Style.RESET_ALL)

                while True:
                    try:
                        amount = float(input(Fore.BLUE + "Enter expense amount: " + Style.RESET_ALL))
                        break
                    except ValueError as error:
                        print(Fore.LIGHTRED_EX + f"Invalid input: {error}. Please enter a valid amount:" + Style.RESET_ALL)

                new_expense_row = [month, date, category, description, amount]
                self.expenses_worksheet.append_row(new_expense_row)

                print(f"\n{Fore.GREEN + Style.BRIGHT}New expense for {month} on {date} added successfully!{Style.RESET_ALL}")
                self.display_worksheet("expenses")  # Display updated expenses after adding

                print(Fore.GREEN + Style.BRIGHT + "\n****************************************************" + Style.RESET_ALL)

                print(Fore.BLUE + "\nWhat would like to do next?" + Style.RESET_ALL)
                return get_main_user_choice()

            except ValueError as error:
                print(Fore.LIGHTRED_EX + f"Invalid input: {error}. Please enter a valid month or date." + Style.RESET_ALL)
                
#CALL WELCOME AND USER CHOICE functions
def main():
    welcome()
    get_main_user_choice()

main()             


    

