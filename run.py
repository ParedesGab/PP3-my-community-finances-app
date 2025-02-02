import gspread
from google.oauth2.service_account import Credentials
from colorama import init, Fore, Style, Back
from datetime import datetime
import re


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('my_finances')


def welcome():
    """Displays a welcome message with color."""
    init()
    rim = f"{Fore.GREEN + Style.BRIGHT}======================{Style.RESET_ALL}"
    print(f"""
    {rim} WELCOME TO MyFinances APP! {rim}
    
    This expense tracker will help you monitor your 2025 income and expenses!
    Are you ready to understand your spending habits?\n
    Let's go!🚀 

    {rim}{rim}{rim}
    """)


def show_application_instructions():
    """Displays instructions for how to use the application."""
    instructions = f"""
    {Fore.GREEN + Style.BRIGHT}== APPLICATION INSTRUCTIONS == {Style.RESET_ALL}

    Welcome to My finances app! Here is how you can use your application:\n

    {Fore.BLUE} 1. Add New Income:{Style.RESET_ALL}

       - You can add income records to track your earnings.
       - Each income entry consists of:
         → {Fore.YELLOW}Month{Style.RESET_ALL}: The month the income was earned.
            E.g., January, February.
         → {Fore.YELLOW}Source{Style.RESET_ALL}: The source of the income.
            E.g., Salary, Freelance.
         → {Fore.YELLOW}Amount{Style.RESET_ALL}: The amount earned in EUR.
            E.g., 10.00.

    {Fore.BLUE} 2. Add New Expense:{Style.RESET_ALL}

       - You can record your expenses to monitor your spending.
       - Each expense entry consists of:
         → {Fore.YELLOW}Month{Style.RESET_ALL}: The month the expense occurred.
            E.g., January, February.
         → {Fore.YELLOW}Category{Style.RESET_ALL}: The category of the expense.
            E.g., Rent, Groceries.
         → {Fore.YELLOW}Description{Style.RESET_ALL}: Expense description.
            E.g., Monthly Rent.
         → {Fore.YELLOW}Amount{Style.RESET_ALL}: The amount spent in EUR.
            E.g., 10.00.

    {Fore.BLUE} 3. Generate Monthly Finance Report:{Style.RESET_ALL}

       - Select a month to generate a detailed income and expenses report.
       - The report will display:
         → Total Income for the selected month.
         → Total Expenses for the selected month.
         → Your cash balance (Income - Expenses).
         → A breakdown of expenses by category.
         → Your highest expense category.

    {Fore.BLUE} 4. Display All Income and Expenses:{Style.RESET_ALL}

       - View all your records from the "income" and "expenses" worksheets.
       - This option shows all your data in a table format.

    {Fore.BLUE} 5. Exit Program:{Style.RESET_ALL}

       - Close the application. Don't worry; all your data is stored! ✨
    """
    print(instructions)
    rim = f"{Fore.GREEN + Style.BRIGHT}======================{Style.RESET_ALL}"
    print(f"{rim}{rim}{rim}")

    #press enter to continue or 5 to exit


def get_menu_user_choice():
    """Gets the user's choice from the menu options."""
    while True:
        print(f"""
    Press 0 to check the application instructions.
    Press 1 to add a new income entry (Month, Source, and Amount).
    Press 2 to add a new expense entry (Month, Category, Description, Amount).
    Press 3 to check your monthly finance report!
    Press 4 to view all your Income and Expenses!
    Press 5 to exit the program.
        """)

        try:
            choice_message = (
                Fore.BLUE + Style.BRIGHT +
                "Enter your option (0-5) and press enter:\n" +
                Style.RESET_ALL
            )
            user_input = input(choice_message)

        # Check for empty input
            if not user_input:
                raise ValueError(
                    Fore.LIGHTRED_EX +
                    "Empty input: Please enter a number between 0 and 5 "
                    "without spaces or special characters.\n" +
                    Style.RESET_ALL
                )

            if not is_valid_number(user_input):
                raise ValueError(
                    Fore.LIGHTRED_EX +
                    "Invalid input: Please enter a number between 0 and 5 "
                    "without spaces or special characters.\n" +
                    Style.RESET_ALL
                )

        # Attempt conversion to integer, to handle potential errors
            option = int(user_input)

        # Validate the option
            validate_user_choice(option)
        # Return the handle_user_option function
            return handle_user_option(option)

        except ValueError as error:
            print(error)


def validate_user_choice(user_choice):
    """Validates the user's choice."""
    if not 0 <= user_choice <= 5:
        raise ValueError(
                    Fore.LIGHTRED_EX +
                    "Invalid input: Please enter a number between 0 and 5 "
                    "without spaces or special characters.\n" +
                    Style.RESET_ALL
                )


def is_valid_number(input_value):
    """Checks if the input value is a valid number."""
    if not input_value.isdigit() or input_value.startswith("+"):
        return False
    return True


def handle_user_option(option):
    """Handles user option."""

    if option == 0:
        show_application_instructions()

    if option == 1:
        finance_manager = FinanceManager()
        finance_manager.add_new_income_to_income_worksheet()

    elif option == 2:
        finance_manager = FinanceManager()
        finance_manager.add_new_expense_to_expense_worksheet()

    elif option == 3:
        finance_manager = FinanceManager()
        return finance_manager.generate_monthly_finance_report()

    elif option == 4:
        finance_manager = FinanceManager()

        income_header = Fore.BLUE + "\n**Income Data**" + Style.RESET_ALL
        print(income_header)
        finance_manager.display_worksheet("income")

        expenses_header = Fore.BLUE + "\n**Expenses Data**" + Style.RESET_ALL
        print(expenses_header)

        finance_manager.display_worksheet("expenses")

        print(Fore.GREEN + Style.BRIGHT + "\n**************" + Style.RESET_ALL)
        menu_prompt = (
            Fore.BLUE + "What would you like to do next?" + Style.RESET_ALL
        )
        print(menu_prompt)
        return get_menu_user_choice()

    elif option == 5:
        exit_message = f"""
        {Fore.GREEN + Style.BRIGHT}
        ✨ Your finances are in good hands ✨
            Goodbye and See you next time!{Style.RESET_ALL}
        """
        print(exit_message)
        exit()


class FinanceManager:

    def __init__(self):
        self.income_worksheet = SHEET.worksheet("income")
        self.expenses_worksheet = SHEET.worksheet("expenses")

    def get_worksheet_data(self, worksheet):
        """Gets all data from a worksheet"""
        worksheet = SHEET.worksheet(worksheet)
        all_values = worksheet.get_all_values()
        return all_values

    def add_new_income_to_income_worksheet(self):
        """Adds a new income record to the "income" worksheet."""

        income_message = f"""
{Fore.GREEN + Style.BRIGHT}**** ADD A NEW INCOME RECORD FOR 2025 ****
        {Style.RESET_ALL}
        Please provide the following details in order:

        → {Fore.YELLOW}Month{Style.RESET_ALL}: The month the income was earned.
         (Please provide the complete month name. E.g, January).

        → {Fore.YELLOW}Source{Style.RESET_ALL}: The source of the income.
         (Please ensure it is at least 4 characters long, includes valid words,
         and isn't entirely numeric. E.g., Salary, Freelance, Etsy).

        → {Fore.YELLOW}Amount{Style.RESET_ALL}: The amount earned in EUR.
         (Positive or negative numbers allowed. E.g., 10.00, +10.00, -10.00).
        """
        print(income_message)

        month = self.get_and_validate_month_input()
        source = self.get_and_validate_source_input()
        amount = self.get_and_validate_amount_input()

        new_income_row = [month, source, amount]

        self.income_worksheet.append_row(new_income_row)

        print(
            f"\n{Fore.GREEN + Style.BRIGHT}"
            f"New income for {month} from {source} (EUR {amount:.2f}) "
            f"added successfully!{Style.RESET_ALL}"
        )
        self.display_worksheet("income")

        print(Fore.GREEN + Style.BRIGHT + "\n*****" + Style.RESET_ALL)
        print(
            Fore.BLUE +
            "\nWhat would you like to do next?" +
            Style.RESET_ALL
        )
        return get_menu_user_choice()

    def get_and_validate_month_input(self):
        """Prompts the user to enter a month name and validates the input."""
        while True:

            prompt_month = (
                Fore.BLUE + "Please enter the month name (e.g., january):\n" +
                Style.RESET_ALL
            )

            user_month = input(prompt_month).strip().lower()

            try:
                datetime.strptime(user_month, "%B")
                month = user_month.title()
                return month

            except ValueError as error:
                print(Fore.LIGHTRED_EX + "Invalid input: Please enter a month name." +
                    Style.RESET_ALL)              

    def get_and_validate_source_input(self):
        """Prompts the user to enter a source name and validates the input."""
        while True:
            prompt_source = (
                Fore.BLUE + "Please enter the income source (minimum 4 characters):\n" +
                Style.RESET_ALL
            )

            user_source = input(prompt_source).strip().lower()

            if len(user_source) >= 4 and re.search('[a-zA-Z]', user_source) and not user_source.isdigit():
                    return user_source
            else:
                print(Fore.LIGHTRED_EX + "Invalid input: Ensure it is at least 4 characters long, contains alphabetic characters, and is not purely numeric." +
                    Style.RESET_ALL)

    def get_and_validate_amount_input(self):
        """Prompts the user to enter a  amount in EUR and validates the input."""
        while True:
            prompt_amount= (
                Fore.BLUE + "Please enter the amount (EUR):\n" +
                Style.RESET_ALL
            )   
            try:
                user_amount = float(input(prompt_amount).strip())
                return user_amount
            except ValueError as error:
                print(
                    Fore.LIGHTRED_EX +
                    f"Invalid input: Please enter a valid amount.\n" +
                    Style.RESET_ALL
                )

    # CHECK IF MONTH SELECTED HAS DATA (for generate_monthly_finance_report)
    def month_has_data(self, worksheet_data, month):
        """Checks if month data exists in a worksheet."""
        for row in worksheet_data:
            if row[0].lower() == month.lower():
                return True
        return False

    # CALCULATE TOTAL AMOUNT (for generate_monthly_finance_report)
    def calculate_total_amount(self, worksheet_data, month, amount_col_index):
        """Calculates the total amount for the given month and worksheet."""
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
        """Calculate expenses per category in a given month."""
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
        """Finds the category with the maximum expense"""
        max_category = max(expenses_by_category, key=expenses_by_category.get)
        max_amount = expenses_by_category[max_category]

        return max_category, max_amount

    # IF "y": SHOW EXPENSES DETAILS (for generate_monthly_finance_report)
    def show_monthly_expenses_details(self, month):
        """Displays detailed expense information for a given month."""
        print(
            f"{Fore.GREEN + Style.BRIGHT}\n"
            f"Calculating Your {month} expenses by category...\n"
            f"{Style.RESET_ALL}"
        )

        # Show expenses per category
        expenses_data = self.get_worksheet_data("expenses")
        expenses_by_category = self.calc_expenses_by_category(
            expenses_data, month
            )

        for category, amount in expenses_by_category.items():
            print(f"→ {category}: EUR {amount:.2f}\n")

        # Show max expense by category
        max_category, max_amount = self.max_expense_by_category(
            expenses_by_category
            )
        print(
            f"{Fore.GREEN + Style.BRIGHT}🎯 HIGHEST EXPENSE:{Style.RESET_ALL} "
            f"{max_category.upper()} (EUR {max_amount:.2f})\n"
        )

    # MONTHLY FINANCE REPORT
    def generate_monthly_finance_report(self):
        """Generates and displays the monthly finance report."""
        print(
            Fore.GREEN + Style.BRIGHT +
            "\n  ✨✨✨✨  MY MONTHLY FINANCE REPORT  ✨✨✨✨\n " +
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

                total_month_income = self.calculate_total_amount(
                    income_data, month, 2
                    )
                total_month_expenses = self.calculate_total_amount(
                    expenses_data, month, 4
                    )

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
                        f"🚨🚨 Attention! Negative cash balance!:"
                        f" EUR{cash_balance: .2f}\n" +
                        Style.RESET_ALL
                    )

                monthly_expenses_details = self.show_monthly_expenses_details(
                    month
                    )

                # Ask user: What to do next?
                print(Fore.GREEN + Style.BRIGHT + "\n*****" + Style.RESET_ALL)
                print(
                    Fore.BLUE +
                    "\nWhat would you like to do next?" +
                    Style.RESET_ALL
                )
                return get_menu_user_choice()

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
                return get_menu_user_choice()

    # IF USER OPTION == 2  (Check my income and expense!)
    def display_worksheet(self, worksheet):
        """Gets data from a given worksheet."""
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

# CALL WELCOME AND USER CHOICE functions
def main():
    welcome()
    get_menu_user_choice()


main()
