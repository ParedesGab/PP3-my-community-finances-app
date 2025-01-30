import gspread
from google.oauth2.service_account import Credentials
from colorama import init, Fore, Style, Back
from datetime import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Create constant variables
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('my_finances')


# WELCOME MESSAGE
def welcome():
    """
    Displays a welcome message with color.
    """
    init()
    border = f"{Fore.GREEN + Style.BRIGHT}=============={Style.RESET_ALL}"
    welcome_message = f"""
    \n{border} WELCOME TO MyFinances APP! {border}\n
    This expense tracker will help you monitor your income and expenses
    to understand your spending habits!\n
    Ready to start? Let's go! 🚀\n
{border}{border}{border}{border}
    """
    print(welcome_message)


# GET USER CHOICE
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
            option = int(input("\nEnter your choice (1-4):\n"))

        # Validate the data
            validate_user_choice(option)
        # return the handle_user_option function
            return handle_user_option(option)

        except ValueError as error:
            print(Fore.LIGHTRED_EX + f"{error}\n" + Style.RESET_ALL)


# VALIDATE USER CHOICE (for get_main_user_choice)
def validate_user_choice(user_choice):
    """
    Validates the user's choice.
    """
    if not 1 <= user_choice <= 5:
        error_message = f"{Fore.LIGHTRED_EX}Invalid choice! " \
                f"Please enter a number between 1 and 5.{Style.RESET_ALL}"
        raise ValueError(error_message)


# HANDLE THE USER SELECTION (for get_main_user_choice)
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

        print(Fore.GREEN + Style.BRIGHT + "\n**************" + Style.RESET_ALL)
        print(
            Fore.BLUE +
            "\nWhat would you like to do next?" +
            Style.RESET_ALL
        )
        return get_main_user_choice()

    elif option == 3:
        finance_manager = FinanceManager()
        finance_manager.add_new_income_to_income_worksheet()

    elif option == 4:
        finance_manager = FinanceManager()
        finance_manager.add_new_expense_to_expense_worksheet()

    elif option == 5:
        exit_message = (
            f"{Fore.GREEN + Style.BRIGHT}✨ Your finances are in good hands ✨ "
            f"Goodbye and See you next time!\n{Style.RESET_ALL}"
        )
        print(exit_message)
        exit()


class FinanceManager:

    # MAKE THE WORKSHEETS ACCESSIBLE FOR THE CLASS METHODS
    def __init__(self):
        self.income_worksheet = SHEET.worksheet("income")
        self.expenses_worksheet = SHEET.worksheet("expenses")

    # GET ALL DATA FROM A WORKSHEET (for generate_monthly_finance_report)
    def get_worksheet_data(self, worksheet):
        '''
        Gets all data from a worksheet
        '''
        worksheet = SHEET.worksheet(worksheet)
        all_values = worksheet.get_all_values()
        return all_values

    # IF USER OPTION == 1
    # GET and validate MONTH SELECTED (for generate_monthly_finance_report)
    def get_and_validate_month_input(self):
        """
        Prompts the user to enter a month name and validates the input.
        """
        # validate the user's choice:
        while True:
            # Ask User which month they want to see
            prompt_month = (
                f"{Fore.BLUE}"
                f"\nPlease enter the month name (e.g., january):\n"
                f"{Style.RESET_ALL}"
            )
            user_month = input(prompt_month).lower()

            try:
                datetime.strptime(user_month, "%B")
                month = user_month.title()
                return month

            # If choice is invalid: ValueError
            except ValueError as error:
                print(
                    Fore.LIGHTRED_EX +
                    "Invalid month name!" +
                    Style.RESET_ALL
                )

    # CHECK IF MONTH SELECTED HAS DATA (for generate_monthly_finance_report)
    def month_has_data(self, worksheet_data, month):
        """
        Checks if data exists for a specific month in a worksheet.
        """
        for row in worksheet_data:
            if row[0].lower() == month.lower():
                return True
        return False

    # CALCULATE TOTAL AMOUNT (for generate_monthly_finance_report)
    def calculate_total_amount(self, worksheet_data, month, amount_col_index):
        """
        Calculates the total amount for the given month and worksheet.
        """
        total_amount = 0
        for row in worksheet_data:
            if row[0].lower() == month.lower():
                try:
                    amount_str = row[amount_col_index].replace(",", "")
                    total_amount += float(amount_str)
                except ValueError as error:
                    print(
                        f"{error}"
                        f"Could not convert amount in {row} to a number."
                    )
        return total_amount

    # CALCULATE EXPENSES BY CATEGORY (for show_monthly_expenses_details)
    def calc_expenses_by_category(self, expenses_data, month):
        """
        Calculate expenses per category in a given month.
        """
        expenses_by_category = {}

        for row in expenses_data:
            if row[0].lower() == month.lower():
                category = row[2]
                try:
                    amount = float(row[4])
                except ValueError:
                    print(
                        f"Warning: Could not convert amount in row"
                        f"{row} to a number."
                    )
                    continue
                if category in expenses_by_category:
                    expenses_by_category[category] += amount
                else:
                    expenses_by_category[category] = amount
        return expenses_by_category

    # MAX EXPENSE PER CATEGORY (for show_monthly_expenses_details)
    def max_expense_by_category(self, expenses_by_category):
        """
        Finds the category with the maximum expense
        """
        max_category = max(expenses_by_category, key=expenses_by_category.get)
        max_amount = expenses_by_category[max_category]

        return max_category, max_amount

    # IF "y": SHOW EXPENSES DETAILS (for generate_monthly_finance_report)
    def show_monthly_expenses_details(self, month):
        """
        Displays detailed expense information for a given month.
        """
        print(
            f"{Fore.GREEN + Style.BRIGHT}\n"
            f"Calculating Your {month} detailed expense report...\n"
            f"{Style.RESET_ALL}"
        )

        # Show expenses per category
        expenses_data = self.get_worksheet_data("expenses")
        expenses_by_category = self.calc_expenses_by_category(expenses_data, month)

        for category, amount in expenses_by_category.items():
            print(f"→ {category}: EUR {amount:.2f}\n")

        # Show max expense by category
        max_category, max_amount = self.max_expense_by_category(expenses_by_category)
        print(
            f"{Fore.GREEN + Style.BRIGHT}🎯 HIGHEST EXPENSE:{Style.RESET_ALL} "
            f"{max_category.upper()} (EUR {max_amount:.2f})\n"
        )

    # MONTHLY FINANCE REPORT
    def generate_monthly_finance_report(self):
        """
        Generates and displays the monthly finance report!
        """
        print("")
        print(
            Fore.GREEN + Style.BRIGHT +
            "\n  ✨✨✨✨  MY MONTHLY FINANCE REPORT  ✨✨✨✨" +
            Style.RESET_ALL
            )

        while True:
            # User inputs the month
            month = self.get_and_validate_month_input()

            # Get all data of a worksheet
            income_data = self.get_worksheet_data("income")
            expenses_data = self.get_worksheet_data("expenses")

            # Check if the month exists within the data
            income_month_data = self.month_has_data(income_data, month)
            expense_month_data = self.month_has_data(expenses_data, month)

            if income_month_data or expense_month_data:
                print(
                    Fore.GREEN + Style.BRIGHT +
                    f"\nCalculating your {month} income and expenses...\n" +
                    Style.RESET_ALL)

                total_month_income = self.calculate_total_amount(income_data, month, 2)
                total_month_expenses = self.calculate_total_amount(expenses_data, month, 4)

                print(f"✅ TOTAL INCOME: EUR{total_month_income: .2f}")
                print(f"✅ TOTAL EXPENSES: EUR{total_month_expenses: .2f}\n")

                # Calculate cash balance
                print(
                    Fore.GREEN + Style.BRIGHT +
                    f"\nCalculating Your {month} cash balance...\n" +
                    Style.RESET_ALL
                    )
                cash_balance = total_month_income - total_month_expenses

                if cash_balance >= 0:
                    print(
                        f"🎉🎉 Congratulations! Positive cash balance!:"
                        f"EUR{cash_balance: .2f}\n"
                        )
                else:
                    print(
                        Fore.LIGHTRED_EX +
                        f"🚨🚨 Attention! Negative cash balance!: EUR{cash_balance: .2f}\n" +
                        Style.RESET_ALL
                    )

                monthly_expenses_details = self.show_monthly_expenses_details(month)

                # Ask user: What to do next?
                print(Fore.GREEN + Style.BRIGHT + "\n*****" + Style.RESET_ALL)
                print(
                    Fore.BLUE +
                    "\nWhat would you like to do next?" +
                    Style.RESET_ALL
                )
                return get_main_user_choice()

            else:
                print(
                    f"{Fore.LIGHTRED_EX}\nThere is no data for {month} yet..."
                    f"{Style.RESET_ALL}"
                    )
                print(
                    Fore.BLUE +
                    "\nWhat would you like to do next?" +
                    Style.RESET_ALL
                )
                return get_main_user_choice()

    # IF USER OPTION == 2  (Check my income and expense!)
    def display_worksheet(self, worksheet):
        '''
        get data from a given worksheet.
        '''
        print(
            f"\n{Fore.GREEN + Style.BRIGHT}"
            f"Getting Your {worksheet.capitalize()} data...\n"
            f"{Style.RESET_ALL}"
        )

        all_worksheet_values = self.get_worksheet_data(worksheet)

        # Get header row
        header_row = all_worksheet_values[0]

        # Get data rows
        data_rows = all_worksheet_values[1:]

        # Print header
        print(" | ".join(header_row))
        print("-" * (len(header_row) * 9))

        # Display All income or expenses data
        for row in data_rows:
            print(" | ".join(row))
            print("-" * (len(row) * 9))

    # IF USER OPTION == 3 (Add new expenses)
    def add_new_income_to_income_worksheet(self):
        """
        Adds a new income record to the "income" worksheet.
        """
        print(
            Fore.GREEN + Style.BRIGHT +
            "\n TO ADD A NEW INCOME:" +
            Style.RESET_ALL
        )

        month = self.get_and_validate_month_input()
        prompt_source = (
            Fore.BLUE +
            "Enter income source:\n" +
            Style.RESET_ALL
        )
        source = input(prompt)
        while True:
            try:
                prompt_amount = (
                    Fore.BLUE +
                    "Enter income amount:\n" +
                    Style.RESET_ALL
                )
                amount = float(input(prompt))

                new_income_row = [month, source, amount]

                self.income_worksheet.append_row(new_income_row)

                print(
                    f"\n{Fore.GREEN + Style.BRIGHT}"
                    f"New income for {month} from {source} (EUR {amount:.2f})"
                    f"added successfully!{Style.RESET_ALL}"
                )
                self.display_worksheet("income")

                print(Fore.GREEN + Style.BRIGHT + "\n*****" + Style.RESET_ALL)
                print(
                    Fore.BLUE +
                    "\nWhat would you like to do next?" +
                    Style.RESET_ALL
                )
                return get_main_user_choice()

            except ValueError as error:
                print(
                    Fore.LIGHTRED_EX +
                    f"Invalid input: {error}. Please enter a valid amount.\n" +
                    Style.RESET_ALL
                )

    # IF USER OPTION == 4 (Add new expenses)
    def add_new_expense_to_expense_worksheet(self):
        """
        Adds a new expense record to the "expenses" worksheet.
        Ensures consistency between month and date.
        """
        while True:
            try:
                month = self.get_and_validate_month_input()

                # Date
                prompt_date = (
                    Fore.BLUE +
                    "Enter expense date (YYYY-MM-DD):\n" +
                    Style.RESET_ALL
                    )
                date = input(prompt_date)
                # Validate date format and consistency with month
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                if date_obj.month != datetime.strptime(month, "%B").month:
                    raise ValueError(f"'{date}' does not match the '{month}'")

                # Category
                prompt_category = (
                    Fore.BLUE +
                    "Enter expense category:\n" +
                    Style.RESET_ALL
                    )
                category = input(prompt_category)

                # Description
                prompt_description = (
                    Fore.BLUE +
                    "Enter expense description:\n" +
                    Style.RESET_ALL
                )
                description = input(prompt_description)

                # Amount
                while True:
                    try:
                        prompt_amount = (
                            Fore.BLUE +
                            "Enter expense amount:\n" +
                            Style.RESET_ALL
                        )
                        amount = float(input(prompt_amount))
                        break
                    except ValueError as error:
                        print(
                            Fore.LIGHTRED_EX +
                            f"Error: {error}. Please enter a valid amount:" +
                            Style.RESET_ALL)

                new_expense_row = [month, date, category, description, amount]
                self.expenses_worksheet.append_row(new_expense_row)

                print(
                    f"\n{Fore.GREEN + Style.BRIGHT}"
                    f"New expense for {month} on {date} added successfully!"
                    f"{Style.RESET_ALL}"
                )
                self.display_worksheet("expenses")

                print(Fore.GREEN + Style.BRIGHT + "\n*****" + Style.RESET_ALL)

                print(
                    Fore.BLUE +
                    "\nWhat would you like to do next?" +
                    Style.RESET_ALL
                )
                return get_main_user_choice()

            except ValueError as error:
                print(
                    Fore.LIGHTRED_EX +
                    f"Error: {error}. Please enter a valid month/date." +
                    Style.RESET_ALL)


# CALL WELCOME AND USER CHOICE functions
def main():
    welcome()
    get_main_user_choice()


main()
