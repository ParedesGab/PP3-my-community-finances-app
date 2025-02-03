import gspread
from google.oauth2.service_account import Credentials
from colorama import init, Fore, Style, Back
from datetime import datetime
import re
from tabulate import tabulate


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
    """)


def show_application_instructions():
    """Displays instructions for how to use the application."""
    instructions = f"""
    {Fore.GREEN + Style.BRIGHT}==== APPLICATION INSTRUCTIONS ====
    {Style.RESET_ALL}

    Welcome to MyFinances App! Here is how you can use your application:\n

    {Fore.BLUE} 1. Add New Income:{Style.RESET_ALL}

       - You can add income records to track your earnings in 2025.
       - Each income entry consists of:
         → {Fore.YELLOW}Month{Style.RESET_ALL}: Income month.
            E.g., January, February.
         → {Fore.YELLOW}Source{Style.RESET_ALL}: The source of the income.
            E.g., Salary, Freelance.
         → {Fore.YELLOW}Amount{Style.RESET_ALL}: The amount earned in EUR.
            E.g., 10.00.

    {Fore.BLUE} 2. Add New Expense:{Style.RESET_ALL}

       - You can record your expenses to monitor your spending in 2025.
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
       - The 2025 report will display:
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
    
    prompt_for_menu_or_exit()


def prompt_for_menu_or_exit():
    """Prompts the user to return to the Menu or to exit the program."""
    print("-" * 75)
    print(Fore.BLUE + "\nWhat would like to do next?" + Style.RESET_ALL)
    
    while True:
        print(f"""
        Press M to go back to the MENU.
        Press E to EXIT the program.
        """)
        try:
            choice_message = (
                Fore.BLUE + Style.BRIGHT +  
                "Enter your choice (M or E) and press enter:\n" +
                Style.RESET_ALL
            )
            user_input = input(choice_message).strip().upper()
            if user_input == "M":
                return get_menu_user_choice()
            elif user_input == "E":
                exit_program()
            else:
                raise ValueError(Fore.LIGHTRED_EX +
                "Invalid input. Please press 'M' to return to the menu or '5' to exit." +
                 Style.RESET_ALL
                )
        except ValueError as error:
            print(error)


def get_menu_user_choice():
    """Gets the user's choice from the menu options."""
    while True:
        print(f"""
    {Fore.GREEN + Style.BRIGHT}==== MENU OPTIONS ===={Style.RESET_ALL}

    Press 0 to check the application instructions.
    Press 1 to add a new income entry (Month, Source, and Amount).
    Press 2 to add a new expense entry (Month, Category, Description, Amount).
    Press 3 to view all your income and expenses.
    Press 4 to check your Monthly Finance Report! 
    Press E to exit the program.
        """)

        try:
            choice_message = (
                Fore.BLUE + Style.BRIGHT +
                "\nEnter your choice (0-5) and press enter:\n" +
                Style.RESET_ALL
            )
            user_input = input(choice_message)

        # Check for empty input
            if not user_input:
                raise ValueError(
                    Fore.LIGHTRED_EX +
                    "Empty input:  enter a number between 0 and 5 "
                    "without spaces or special characters.\n" +
                    Style.RESET_ALL
                )

            if not is_valid_number(user_input):
                raise ValueError(
                    Fore.LIGHTRED_EX +
                    "Invalid input:  enter a number between 0 and 5 "
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
                    "Invalid input:  enter a number between 0 and 5 "
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

    finance_manager = FinanceManager()

    if option == 0:
        show_application_instructions()

    elif option == 1:
        finance_manager.add_new_income_to_income_worksheet()

    elif option == 2:
        finance_manager.add_new_expense_to_expense_worksheet()

    elif option == 3:
        # Display income data first
        finance_manager.display_worksheet("income")

        # Display expenses data after income is displayed
        finance_manager.display_worksheet("expenses")

         # Prompt user for next action after both are displayed
        prompt_for_menu_or_exit()

    elif option == 4:
        return finance_manager.generate_monthly_finance_report()

    elif option == "E":
        return exit_program()


def exit_program():
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
    {Fore.GREEN + Style.BRIGHT}==== ADD A NEW INCOME RECORD FOR 2025 ====
        {Style.RESET_ALL}
         Please provide the following details in order:

        → {Fore.YELLOW}Month{Style.RESET_ALL}: The month the income was earned.
          (Enter complete month name. E.g, January).

        → {Fore.YELLOW}Source{Style.RESET_ALL}: The source of the income.
          (Ensure it is at least 4 characters long, includes valid words,
          and isn't entirely numeric. E.g., Salary, Freelance, Etsy).

        → {Fore.YELLOW}Amount{Style.RESET_ALL}: The amount earned in EUR.
          (E.g., 1500.00).
        """
        print(income_message)

        month = self.get_and_validate_month_input()
        source = self.get_and_validate_source_input()
        amount = self.get_validated_and_normalized_amount()
        formatted_amount = self.format_amount_for_display(amount)

        new_income_row = [month, source, formatted_amount]

        self.income_worksheet.append_row(new_income_row)

        print("\nStoring your new income entry ...")

        print(f"""
        {Fore.GREEN + Style.BRIGHT}
        New income for {month}, 2025 from source: {source} (EUR {formatted_amount})
        stored successfully!
        {Style.RESET_ALL}
        """)

        print("-" * 75)
        print(Fore.BLUE + "\nWhat would like to do next?" + Style.RESET_ALL)

        # Prompt the user to choose what to do next
        while True:
            print(f"""
            Press 1 to add ANOTHER INCOME entry.
            Press 2 to add an expense entry.
            Press M to go back to the MENU.
            Press E to EXIT the program.
            """)
            choice_message = (
                Fore.BLUE + Style.BRIGHT +  
                "Enter your choice (1, 2, M or E) and press enter:\n" +
                Style.RESET_ALL
            )
            user_input = input(choice_message).strip().upper()
            if user_input == "1":
                return self.add_new_income_to_income_worksheet()
            elif user_input == "2":
                return self.add_new_expense_to_expense_worksheet()
            elif user_input == "M":
                return get_menu_user_choice()
            elif user_input == "E":
                exit_program()
            else:
                print(Fore.LIGHTRED_EX + "Invalid input. Please enter 1, 2, M, or E." + Style.RESET_ALL)

    def add_new_expense_to_expense_worksheet(self):
        """Adds a new expense record to the "expense" worksheet."""

        print(f"""
        {Fore.GREEN + Style.BRIGHT}
        ==== ADD A NEW EXPENSE RECORD FOR 2025 ====
        {Style.RESET_ALL}
         Please provide the following details in order:

        → {Fore.YELLOW}Month{Style.RESET_ALL}: The month the income was earned.
          (Enter the complete month name. E.g, January).
        → {Fore.YELLOW}Category{Style.RESET_ALL}: The source of the income.
          (Ensure it is at least 4 characters long, includes valid words,
          and isn't entirely numeric. E.g., Salary, Freelance).
        → {Fore.YELLOW}Description{Style.RESET_ALL}: A expense description.
          (Ensure it is at least 4 characters long, includes valid words,
          and isn't entirely numeric. E.g., Weekly groceries).
        → {Fore.YELLOW}Amount{Style.RESET_ALL}: The amount earned in EUR.
          (E.g., 1500.00).
        """)

        month = self.get_and_validate_month_input()
        category = self.get_and_validate_category_input()
        description = self.get_and_validate_description_input()
        amount = self.get_validated_and_normalized_amount()
        formatted_amount = self.format_amount_for_display(amount)

        new_expense_row = [month, category, description, formatted_amount]
        self.expenses_worksheet.append_row(new_expense_row)

        print("\nStoring your new expense entry ...")

        print(f"""
        {Fore.GREEN + Style.BRIGHT}
        New expense for {month}, 2025 with category: '{category}'
        and description: '{description}' ({formatted_amount} EUR), added successfully!
        {Style.RESET_ALL}
        """)

        print("-" * 75)
        print(Fore.BLUE + "\nWhat would like to do next?" + Style.RESET_ALL)

        # Prompt the user to choose what to do next
        while True:
            print(f"""
            Press 1 to add income entry.
            Press 2 to add ANOTHER EXPENSE entry.
            Press M to go back to the MENU.
            Press E to EXIT the program.
            """)
            choice_message = (
                Fore.BLUE + Style.BRIGHT +  
                "Enter your choice (1, 2, M or E) and press enter:\n" +
                Style.RESET_ALL
            )
            user_input = input(choice_message).strip().upper()
            if user_input == "1":
                return self.add_new_income_to_income_worksheet()
            elif user_input == "2":
                return self.add_new_expense_to_expense_worksheet()
            elif user_input == "M":
                return get_menu_user_choice()
            elif user_input == "E":
                exit_program()
            else:
                print(Fore.LIGHTRED_EX + "Invalid input. Please enter 1, 2, M, or E." + Style.RESET_ALL)

    def get_and_validate_month_input(self):
        """Prompts the user to enter a month name and validates the input."""
        while True:

            prompt_month = (
                Fore.BLUE + "Enter the month name (e.g., january):\n" +
                Style.RESET_ALL
            )

            user_month = input(prompt_month).strip().lower()

            try:
                datetime.strptime(user_month, "%B")
                month = user_month.title()
                return month

            except ValueError as error:
                print(
                    Fore.LIGHTRED_EX +
                    "Invalid input: Enter a month name." +
                    Style.RESET_ALL
                )
    def get_and_validate_input(self, prompt, min_length=4, require_alpha=True):
        """
        Prompts the user for input and validates it based on various criteria.
        """
        while True:
            user_input = input(Fore.BLUE + prompt + Style.RESET_ALL).strip()

            if len(user_input) < min_length:
                print(f"""
                    {Fore.LIGHTRED_EX}
                    Invalid input: Minimun {min_length} characters long,
                    contain alphabetic characters, and not be purely numeric
                    {Style.RESET_ALL}
                """)
                continue

            if require_alpha and not re.search('[a-zA-Z]', user_input):
                print(f"""
                    {Fore.LIGHTRED_EX}
                    Invalid input: Minimun {min_length} characters long,
                    contain alphabetic characters, and not be entirely numeric.
                    {Style.RESET_ALL}
                """)
                continue

            if user_input.isdigit():
                print(
                    Fore.LIGHTRED_EX +
                    "Invalid input: Cannot be entirely numeric." +
                    Style.RESET_ALL
                )
                continue

            return user_input

    def get_and_validate_source_input(self):
        """
        Ensures that source, description and category inputs meet minimum length
        and alphabetic character requirements.
        """
        prompt_source = (
            Fore.BLUE + "Enter the income source (minimum 4 characters):\n" +
            Style.RESET_ALL
        )
        return self.get_and_validate_input(prompt_source)
    
    def get_and_validate_category_input(self):
        """Prompts the user to enter a category name and validates the input."""
        prompt_category = (
            Fore.BLUE + "Enter the category (minimum 4 characters):\n" +
            Style.RESET_ALL
        )
        return self.get_and_validate_input(prompt_category)

    def get_and_validate_description_input(self):
        """Prompts the user to enter a description name and validates the input."""
        prompt_description = (
            Fore.BLUE + "Enter the description (minimum 4 characters):\n" +
            Style.RESET_ALL
        )
        return self.get_and_validate_input(prompt_description)

    def get_validated_and_normalized_amount(self):
        """Prompts the user to enter an amount (EUR) and normalizes and validates the input."""
        while True:
            prompt_amount = (
                Fore.BLUE + "Enter the amount (EUR):\n" +
                Style.RESET_ALL
            )
            amount_input = input(prompt_amount).strip()

            # Do not allow an empty input
            if not amount_input:
                print(
                    Fore.LIGHTRED_EX +
                    "Invalid input: Enter a month name." +
                    Style.RESET_ALL
                )
                continue

            # Remove all non-digit characters (but keep . and , and spaces)
            amount_input = re.sub(r"[^\d., ]", "", amount_input)

            # Remove spaces as potential thousands separators
            amount_input = amount_input.replace(" ", "")

            # Check if there is any comma and no dot. If yes, replace the comma with dot
            if "," in amount_input and "." not in amount_input:
                amount_input = amount_input.replace(",", ".")

            # Check if there is any dot and no comma. If yes, nothing happens
            elif "." in amount_input and "," not in amount_input:
                pass

            # Check if there are both comma and dot. If yes, then it can be two cases:
            # Case a) 12,345.67 (comma is thousand separator and dot is decimal separator)
            # Case b) 12.345,67 (dot is thousand separator and comma is decimal separator)

            elif "." in amount_input and "," in amount_input:

                # find the rightmost occurrence INDEX of either a "." or a ","
                last_separator = max(amount_input.rfind("."), amount_input.rfind(","))

                # Case a) e.g.: 12,345.67 (USA convention)
                if amount_input[last_separator] == ".":
                    amount_input = amount_input.replace(",", "")
                    # Replace only the first found dot
                    amount_input = amount_input.replace(".", ",", 1)
                else:
                    amount_input = amount_input.replace(".", "")

                # Ensure amount_input can be used with float()
            amount_input = amount_input.replace(",", ".")

            try:
                amount = float(amount_input)
                if amount < 0:
                    raise ValueError("Amount cannot be negative.")
                return amount
            except ValueError:
                print(Fore.LIGHTRED_EX + "Invalid amount format. Please use digits, '.', or ',' as separators.\n" + Style.RESET_ALL)

    def format_amount_for_display(self, amount):
        """Formats the amount for display (European format)."""
        formatted_amount = "{:,.2f}".format(amount).replace(",", "X").replace(".", ",").replace("X", ".")

        return formatted_amount # Always EUR and always after the amount

    def display_worksheet(self, worksheet):
        """Gets data from a given worksheet."""
        all_worksheet_values = self.get_worksheet_data(worksheet)

        if not all_worksheet_values:
            print(Fore.LIGHTRED_EX +
            "No data available in this worksheet." + 
            Style.RESET_ALL)
            return

        # Get header row
        header_row = all_worksheet_values[0]

        # Get data rows
        data_rows = all_worksheet_values[1:]

        print(f"""
        {Fore.GREEN + Style.BRIGHT}
        ==== YOUR {worksheet.upper()} DATA IN 2025 ====
        {Style.RESET_ALL}""")

        # Use tabulate to display data in tabular form
        print(f"Getting your {worksheet.capitalize()} data...")
        print(tabulate(data_rows, headers=header_row, tablefmt="pretty"))

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
                    # Get the amount from the worksheet as a string
                    amount_string= row[amount_col_index]
                    # Normalize the string (handle European format)
                    amount_string = amount_string.replace(".", "").replace(",", ".")
                    # Convert string float after normalization
                    total_amount += float(amount_string)
                except ValueError as error:
                    print(
                        f"{error}"
                        f"Could not convert amount in {row} to a number."
                    )
                except Exception as e: # Catch any other potential errors
                    print(Fore.LIGHTRED_EX + f"An error occurred: {e}\n" + Style.RESET_ALL)
        return total_amount

    # CALCULATE EXPENSES BY CATEGORY (for show_monthly_expenses_details)
    def calc_expenses_by_category(self, expenses_data, month):
        """Calculate expenses per category in a given month."""
        expenses_by_category = {}

        for row in expenses_data:
            if row[0].lower() == month.lower():
                category = row[1]
                try:
                    # Get the amount from the worksheet as a string
                    amount_string = row[3]
                    # Normalize the string (handle European format)
                    amount_string = amount_string.replace(".", "").replace(",", ".")
                    # Convert string float after normalization
                    amount = float(amount_string)
                
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
        expenses_by_category = self.calc_expenses_by_category(expenses_data, month)

        for category, amount in expenses_by_category.items():
            print(f"→ {category}: EUR {amount:.2f}\n")

        # Show max expense by category
        max_category, max_amount = self.max_expense_by_category(
            expenses_by_category
            )
        print(
            f"{Fore.GREEN + Style.BRIGHT}🔥 HIGHEST EXPENSE:{Style.RESET_ALL} "
            f"{max_category.upper()} ({max_amount:.2f} EUR)\n"
        )

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
                    expenses_data, month, 3
                    )

                print(f"✅ TOTAL INCOME:{total_month_income: .2f} EUR")
                print(f"✅ TOTAL EXPENSES:{total_month_expenses: .2f} EUR\n")

                # Calculate cash balance
                print(
                    Fore.GREEN + Style.BRIGHT +
                    f"\nCalculating Your {month} cash balance...\n" +
                    Style.RESET_ALL
                    )
                cash_balance = total_month_income - total_month_expenses
                #cash_balance = cash_balance.replace(".", "").replace(",", ".")

                if cash_balance >= 0:
                    print(
                        f"🎉🎉 Congratulations! Positive cash balance!:"
                        f"{cash_balance: .2f} EUR\n"
                        )
                else:
                    print(
                        Fore.LIGHTRED_EX +
                        f"🚨🚨 Attention! Negative cash balance!:"
                        f"{cash_balance: .2f}EUR\n" +
                        Style.RESET_ALL
                    )

                monthly_expenses_details = self.show_monthly_expenses_details(
                    month
                    )

                return prompt_for_menu_or_exit()

            else:
                print(
                    f"{Fore.LIGHTRED_EX}\nThere is no data for {month} yet..."
                    f"{Style.RESET_ALL}"
                    )
                return prompt_for_menu_or_exit()

# CALL WELCOME AND USER CHOICE functions
def main():
    welcome()
    get_menu_user_choice()


main()
