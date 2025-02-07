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

# List of valid expense categories
CATEGORIES = [
    "Housing", "Transportation", "Food", "Personal Care", "Healthcare",
    "Entertainment", "Shopping", "Education", "Travel", "Gifts", "Other"
]


def welcome():
    """Displays a welcome message with color."""
    init()
    rim = f"{Fore.GREEN + Style.BRIGHT}================={Style.RESET_ALL}"
    print(f"""
    {rim} Welcome to the FinancialSurvey2025! {rim}

    This application collects information about income and expenses
    to better understand the economic landscape!

    Your participation will remain anonymous.
    Thank you for helping us gain a deeper understanding of personal finances!

    Let's get started! 🚀
    """)


def exit_program():
    """Displays a farewell message and terminates the program."""
    exit_message = f"""
    {Fore.GREEN + Style.BRIGHT}
    ✨ Thank you for participating in the FinancialSurvey2025! ✨

    Your contribution is greatly appreciated, Goodbye!{Style.RESET_ALL}
    """
    print(exit_message)
    exit()


def prompt_for_menu_or_exit():
    """Prompts the user to return to the Menu or to exit the program."""
    print("-" * 75)
    print(Fore.BLUE + "\nWhat would you like to do next?" + Style.RESET_ALL)
    while True:
        print("""
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
                raise ValueError(
                    Fore.LIGHTRED_EX +
                    "Invalid input. Please press 'M' to return to the menu"
                    " or 'E' to exit." + Style.RESET_ALL)
        except ValueError as error:
            print(error)


def show_application_instructions():
    """Displays instructions for how to use the application."""
    instructions = f"""
    {Fore.GREEN + Style.BRIGHT}==== APPLICATION INSTRUCTIONS ====
    {Style.RESET_ALL}

    Welcome to the FinancialSurvey2025!! App instructions:

    {Fore.BLUE} 1. Add New Income:{Style.RESET_ALL}

       - Please provide your 2025 income(s) information here.
       - Each income entry consists of:
         → {Fore.YELLOW}Month{Style.RESET_ALL}: Income month.
            E.g., January, February.
         → {Fore.YELLOW}Source{Style.RESET_ALL}: The source of the income.
            E.g., Salary, Freelance.
         → {Fore.YELLOW}Amount{Style.RESET_ALL}: The amount earned.
            E.g., 1500.

            Note:
            - Source input is flexible, but informative entries will help
              us build a more informed future!
            - The amount is displayed and stored following the
              standard European currency format (i.e., 1.500,00 EUR).
            - All input fields are required (empty entries are not valid).

    {Fore.BLUE} 2. Add New Expense:{Style.RESET_ALL}

       - Please provide your 2025 expense(s) information here.
       - Each expense entry consists of:
         → {Fore.YELLOW}Month{Style.RESET_ALL}: Expense month.
            E.g., January, February.
         → {Fore.YELLOW}Category{Style.RESET_ALL}: Expense category.

         IMPORTANT: Please choose a category from the following list:
         {Fore.GREEN}
         - Housing
         - Transportation
         - Food
         - Personal Care
         - Healthcare
         - Entertainment
         - Shopping
         - Education
         - Travel
         - Gifts
         - Other
         {Style.RESET_ALL}
         → {Fore.YELLOW}Description{Style.RESET_ALL}: Expense description.
            Use this field to provide context.
            E.g., for Housing: Monthly Rent, mortgage fee, rent payment, etc.
         → {Fore.YELLOW}Amount{Style.RESET_ALL}: The amount spent.
            E.g., 1500.

            Note:
            - IMPORTANT: Category inputs must be chosen from the list above!
            - Description inputs are flexible but creating
              informative entries will help gain a deeper understanding
              of personal finances!
            - The amount is displayed and stored following the
              standard European currency format (i.e., 1.500,00 EUR).
            - All input fields are required (empty entries are not valid).

    {Fore.BLUE} 3. Display All Income and Expenses:{Style.RESET_ALL}

       - This option displays all 2025 survey responses.
       - It shows the data in a tabular format.

    {Fore.BLUE} 4. View AGGREGATED 2025 MONTHLY FINANCE REPORT{Style.RESET_ALL}

       - Select a month to view the aggregated 2025 financial survey data.
         E.g., January, February.
       - The 2025 report will display:
         → Aggregate total Income for the selected month.
         → Aggregate total Expenses for the selected month.
         → Net finantial balance (Income - Expenses).
         → A breakdown of expenses by category.
         → The highest expense category.



    {Fore.BLUE} E. Exit Program:{Style.RESET_ALL}

       - Close the application. Don't worry; your data remains anonymous ✨
    """
    print(instructions)
    prompt_for_menu_or_exit()


class FinanceManager:
    """
    Manages financial data for the year 2025 by interacting with a Google Sheet.
    This class provides methods to add income and expense records, retrieve data from
    the spreadsheet, calculate totals, generate reports, and display information to the user.
    It handles data validation and formatting for European currency.
    """

    def __init__(self):
        """
        Initializes the FinanceManager object
        and retrieves incomes/expense worksheets.
        """
        # Get the income and expenses worksheets
        self.income_worksheet = SHEET.worksheet("incomes")
        self.expenses_worksheet = SHEET.worksheet("expenses")

    def get_worksheet_data(self, worksheet_name):
        """Gets all data from a specified worksheet"""
        worksheet_name = SHEET.worksheet(worksheet_name)
        all_values = worksheet_name.get_all_values()
        return all_values

    def add_new_income_to_income_worksheet(self):
        """Adds a new income record to the "incomes" worksheet."""
        income_message = f"""
        {Fore.GREEN + Style.BRIGHT}==== ADD A NEW INCOME RECORD FOR 2025 ====
        {Style.RESET_ALL}
         Please provide the following details in order:

        → {Fore.YELLOW}Month{Style.RESET_ALL}: The month the income was earned.
          (Enter complete month name. E.g, January).
        → {Fore.YELLOW}Source{Style.RESET_ALL}: The source of the income.
          (Ensure it is at least 4 characters long, and isn't entirely numeric.
          E.g., Salary, Freelance, Etsy).
        → {Fore.YELLOW}Amount{Style.RESET_ALL}: The amount earned (e.g, 1500).
          (Must be a positive number (no "-" sign).
          It is displayed in EU currency format. E.g, 1.500, 00 EUR.
        """
        print(income_message)

        month = self.get_and_validate_month_input()
        source = self.get_and_validate_source_input()
        amount = self.get_validated_and_normalized_amount()
        formatted_amount = self.format_amount_for_display(amount)

        new_income_row = [month, source, formatted_amount]

        self.income_worksheet.append_row(new_income_row)

        print("\nStoring your income entry ...")

        print(f"""
        {Fore.GREEN + Style.BRIGHT}
        Thank you! New income for {month}, 2025 from '{source}'
        ({formatted_amount} EUR), stored successfully!
        {Style.RESET_ALL}
        """)

        print("-" * 75)
        # Prompt the user to choose what to do next
        print(
            Fore.BLUE + "\nWhat would you like to do next?" +
            Style.RESET_ALL)
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
                Style.RESET_ALL)
            user_input = input(choice_message).strip().upper()
            if user_input == "1":
                return self.add_new_income_to_income_worksheet()
            elif user_input == "2":
                return self.add_new_expense_to_expense_worksheet()
            elif user_input == "M":
                return get_menu_user_choice()
            elif user_input == "E":
                return exit_program()
            else:
                print(
                    Fore.LIGHTRED_EX +
                    "Invalid input. Please enter 1, 2, M, or E." +
                    Style.RESET_ALL)

    def add_new_expense_to_expense_worksheet(self):
        """Adds a new expense record to the "expense" worksheet."""
        print(f"""
        {Fore.GREEN + Style.BRIGHT}
        ==== ADD A NEW EXPENSE RECORD FOR 2025 ====
        {Style.RESET_ALL}
         Please provide the following details in order:

        → {Fore.YELLOW}Month{Style.RESET_ALL}: The month the income was earned.
          (Enter the complete month name. E.g, January).
        → {Fore.YELLOW}Category{Style.RESET_ALL}: The expense category.
          IMPORTANT: Category input is restricted to the below list!

          Please choose from this list (lowercase names allowed):
          {Fore.YELLOW}
          - Housing
          - Transportation
          - Food
          - Personal Care
          - Healthcare
          - Entertainment
          - Shopping
          - Education
          - Travel
          - Gifts
          - Other
          {Style.RESET_ALL}
        → {Fore.YELLOW}Description{Style.RESET_ALL}: A expense description.
          (Ensure it is at least 4 characters long, and isn't entirely numeric.
          E.g., Weekly groceries).
        → {Fore.YELLOW}Amount{Style.RESET_ALL}: The amount earned (e.g, 1500).
          (Must be a positive number (no "-" sign) and contain only digits
          (no special characters or letters).
          It is displayed in EU currency format. E.g, 1.500, 00 EUR.
        """)

        month = self.get_and_validate_month_input()

        while True:
            category = self.get_and_validate_category_input()
            # Check against the predefined category list
            if category in CATEGORIES:
                # Exit the loop because the category is valid
                break
            else:
                # Display the predefined category list
                print(Fore.LIGHTRED_EX +
                      "\nInvalid category. Please choose from the list:\n" +
                      Style.RESET_ALL)
                for category in CATEGORIES:
                    print(f"→ {category}")

        description = self.get_and_validate_description_input()
        amount = self.get_validated_and_normalized_amount()
        formatted_amount = self.format_amount_for_display(amount)

        new_expense_row = [month, category, description, formatted_amount]
        self.expenses_worksheet.append_row(new_expense_row)

        print("\nStoring your expense entry ...")

        print(f"""
        {Fore.GREEN + Style.BRIGHT}
        Thank you! New expense for {month}, 2025 for '{category}' 
        ('{description}', {formatted_amount} EUR), added successfully!
        {Style.RESET_ALL}
        """)

        print("-" * 75)
        print(Fore.BLUE + "\nWhat would you like to do next?" +
              Style.RESET_ALL)

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
                return exit_program()
            else:
                print(
                    Fore.LIGHTRED_EX +
                    "Invalid input. Please enter 1, 2, M, or E." +
                    Style.RESET_ALL)

    def get_and_validate_month_input(self):
        """Prompts the user to enter a month name and validates the input."""
        while True:
            prompt_month = (
                Fore.BLUE + "Enter the month name (e.g., january):\n" +
                Style.RESET_ALL)

            user_month = input(prompt_month).strip().lower()

            try:
                # Interpret the month input as a full month name
                datetime.strptime(user_month, "%B")
                month = user_month.title()
                return month

            except ValueError as error:
                print(
                    Fore.LIGHTRED_EX +
                    "Invalid input: Enter a month name." +
                    Style.RESET_ALL)

    def get_and_validate_input(self, prompt, min_length=4, require_alpha=True):
        """
        Prompts the user for input and validates it based on various criteria.
        Used for the source and the description inputs.
        """
        while True:
            user_input = input(Fore.BLUE + prompt + Style.RESET_ALL).strip()
            # Checks if input length is valid
            if len(user_input) < min_length:
                print(f"""
                    {Fore.LIGHTRED_EX}
                    Invalid input: Must be at least {min_length} characters,
                    contain letters, and not be all numbers.
                    {Style.RESET_ALL}
                """)
                continue
            # Check if input does not have letters
            if require_alpha and not re.search('[a-zA-Z]', user_input):
                print(f"""
                    {Fore.LIGHTRED_EX}
                    Invalid input: Must be at least {min_length} characters,
                    contain letters, and not be all numbers.
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
        Ensures that source, description, category inputs meet minimum length
        and alphabetic character requirements.
        """
        prompt_source = (
            Fore.BLUE + "Enter the income source (minimum 4 characters):\n" +
            Style.RESET_ALL
        )
        return self.get_and_validate_input(prompt_source)

    def get_and_validate_description_input(self):
        """Prompts the user to enter a description and validates the input."""
        prompt_description = (
            Fore.BLUE + "Enter the description (minimum 4 characters):\n" +
            Style.RESET_ALL
        )
        return self.get_and_validate_input(prompt_description)

    def get_and_validate_category_input(self):
        """Prompts the user to enter a category and validates the input."""
        while True:
            print(
                Fore.BLUE +
                "\nSelect a category from this list:\n" +
                Style.RESET_ALL)
            for cat in CATEGORIES:
                print(f"- {cat}")
            prompt_category = (
                Fore.BLUE + "\nEnter the category:\n" + Style.RESET_ALL)
            category_input = input(prompt_category).strip().lower()

            # Check for empty input
            if not category_input:
                print(
                    Fore.LIGHTRED_EX +
                    "Empty input: Please choose a category from the list.\n" +
                    Style.RESET_ALL)
                continue
            # Return the category in title case
            if category_input.title() in CATEGORIES:
                return category_input.title()
            else:
                print(
                    Fore.LIGHTRED_EX +
                    "\nInvalid category. Please choose from the following:\n" +
                    Style.RESET_ALL)

    def get_validated_and_normalized_amount(self):
        """
        Prompts the user to enter an amount, normalizes it,
        and validates the input.
        This function repeatedly prompts the user to enter an amount
        until a valid positive number is provided. It handles various
        input formats, including European (e.g., 1.234,56) and
        US (e.g., 1,234.56) number formatting, and normalizes them to
        a consistent floating-point representation (using a dot as the
        decimal separator). Empty or negative input is rejected.
        """
        while True:
            prompt_amount = (
                Fore.BLUE + "Enter an amount (EUR):\n" +
                Style.RESET_ALL
            )
            amount_input = input(prompt_amount).strip()

            # Do not allow an empty input
            if not amount_input:
                print(
                    Fore.LIGHTRED_EX +
                    "Empty amount: Please enter a positive amount." +
                    Style.RESET_ALL
                )
                continue

            # Reject negative amounts
            if amount_input.startswith("-"):
                print(
                    Fore.LIGHTRED_EX +
                    "Invalid amount: Amount must be positive." +
                    Style.RESET_ALL)
                continue

            # Remove all non-digit characters (but keep . and , and spaces)
            amount_input = re.sub(r"[^\d., ]", "", amount_input)

            # Remove spaces as potential thousands separators
            amount_input = amount_input.replace(" ", "")

            # Check if there is any comma and no dot
            # If yes, replace the comma with dot
            if "," in amount_input and "." not in amount_input:
                amount_input = amount_input.replace(",", ".")

            # Check if there is any dot and no comma. If yes, nothing happens
            elif "." in amount_input and "," not in amount_input:
                pass

            # Check if there are both comma and dot. If yes, then:
            # Case a) 12,345.67 (US format)
            # Case b) 12.345,67 (EU format)

            elif "." in amount_input and "," in amount_input:

                # Find the rightmost occurrence INDEX of either a "." or a ","
                last_dot = amount_input.rfind(".")
                last_comma = amount_input.rfind(",")
                last_separator = max(last_dot, last_comma)

                # Case a) 12,345.67 (US format)
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
                return amount
            except ValueError:
                print(
                    Fore.LIGHTRED_EX +
                    "Invalid amount format. Use digits, dots or commas" +
                    Style.RESET_ALL)

    def format_amount_for_display(self, amount):
        """Formats the amount for display (European format)."""
        fmt = "{:,.2f}".format(amount)
        fmt_amount = fmt.replace(",", "X").replace(".", ",").replace("X", ".")

        # Formated to standard European style (e.g., 1.234,56)
        return fmt_amount

    def display_worksheet(self, worksheet):
        """Gets data from a given worksheet."""
        all_worksheet_values = self.get_worksheet_data(worksheet)

        # Check if the worksheet is completely empty
        if not all_worksheet_values:
            print(
                Fore.LIGHTRED_EX +
                f"No data available in this {worksheet.capitalize()}." +
                Style.RESET_ALL)
            return

        # Check if only the header row exists (no actual data)
        if len(all_worksheet_values) <= 1:
            print(f"\nGetting {worksheet.capitalize()} data...")
            print(
                Fore.YELLOW +
                f"\nNo {worksheet.capitalize()} data has been entered yet!\n" +
                Style.RESET_ALL
            )
            return

        # Get header row
        header_row = all_worksheet_values[0]

        # Get data rows
        data_rows = all_worksheet_values[1:]

        print(f"""
        {Fore.GREEN + Style.BRIGHT}
        ==== {worksheet.upper()} DATA IN 2025 ====
        {Style.RESET_ALL}""")

        # Use tabulate to display data in tabular form
        print(f"Getting {worksheet.capitalize()} data...\n")
        print(tabulate(data_rows, headers=header_row, tablefmt="pretty"))

    def month_has_data(self, worksheet_data, month):
        """Checks if month data exists in a worksheet."""
        for row in worksheet_data:
            if row[0].lower() == month.lower():
                return True
        return False

    def calculate_total_amount(self, worksheet_data, month, amount_col_index):
        """Calculates the total amount for the given month and worksheet."""
        total_amount = 0
        for row in worksheet_data:
            if row[0].lower() == month.lower():
                try:
                    # Get the amount from the worksheet as a string
                    amount = row[amount_col_index]
                    # Normalize the string (handle European format)
                    amount_norm = amount.replace(".", "").replace(",", ".")
                    # Convert string float after normalization
                    total_amount += float(amount_norm)
                except ValueError as error:
                    print(
                        f"Could not convert amount in {row} to a number."
                    )
        return total_amount

    def calc_expenses_by_category(self, expenses_data, month):
        """Calculate expenses per category in a given month."""
        expenses_by_category = {}

        for row in expenses_data:
            if row[0].lower() == month.lower():
                # Normalize category input to title
                category = row[1].title()
                try:
                    # Get the amount from the worksheet as a string
                    amount = row[3]
                    # Normalize the string (handle European format)
                    amount_norm = amount.replace(".", "").replace(",", ".")
                    # Convert string float after normalization
                    amount = float(amount_norm)
                except ValueError:
                    print(f"""
                    {Fore.LIGHTRED_EX}Could not convert amount in {row}
                    to a number."
                    {Style.RESET_ALL}
                    """)
                    continue
                if category in expenses_by_category:
                    expenses_by_category[category] += amount
                else:
                    expenses_by_category[category] = amount
        return expenses_by_category

    def max_expense_by_category(self, expenses_by_category):
        """
        Finds the category with the maximum expense, or None if no expenses.
        Handles the case where expenses_by_category is empty.
        """
        if not expenses_by_category:
            return None, None
        max_category = max(expenses_by_category, key=expenses_by_category.get)
        max_amount = expenses_by_category[max_category]

        return max_category, max_amount

    def show_monthly_expenses_details(self, month):
        """Displays detailed expense information for a given month."""
        print(
            Fore.GREEN + Style.BRIGHT +
            f"\nCalculating {month} Expenses by Category...\n" +
            Style.RESET_ALL)

        # Show expenses per category
        exp_data = self.get_worksheet_data("expenses")
        expenses_by_category = self.calc_expenses_by_category(exp_data, month)

        if not expenses_by_category:
            print(
                Fore.YELLOW +
                f"No expenses found for {month}!" +
                Style.RESET_ALL)
            return

        for category, amount in expenses_by_category.items():
            # Format max_amount for display in European format
            formatted_amount = self.format_amount_for_display(amount)
            print(f"→ {category.upper()}: {formatted_amount} EUR \n")

        # Show max expense by category
        max_category, max_amount = self.max_expense_by_category(
            expenses_by_category)
        # Format max_amount for display in European format
        if max_amount is not None:
            formatted_max_amount = self.format_amount_for_display(max_amount)
        # Handle None case
        else:
            formatted_max_amount = "0.00"

        highest = f"""
        {Fore.GREEN + Style.BRIGHT}🔥 HIGHEST EXPENSE:{Style.RESET_ALL}"""
        print(f"""
        {highest} {max_category.upper()} ({formatted_max_amount} EUR)
        """)

    def generate_monthly_finance_report(self):
        """Generates and displays the monthly finance report."""
        report_message = f"""
        {Fore.GREEN + Style.BRIGHT}
        ✨✨  AGGREGATED 2025 MONTHLY FINANCE REPORT  ✨✨
        {Style.RESET_ALL}

        This report will show you for the month you select:

        → Aggregate Total Income
        → Aggregate Total Expenses
        → Net Finantial Balance:
          Aggregate Total Income - Aggregate Total Expenses
        → A Breakdown of Expenses by Category
        → The Highest Expense Category

        Please enter the month you'd like to review:
        """
        print(report_message)

        while True:
            # User inputs the month
            month = self.get_and_validate_month_input()

            # Get all data of a worksheet
            income_data = self.get_worksheet_data("incomes")
            expenses_data = self.get_worksheet_data("expenses")

            # Check if the month exists within the data
            income_month_data_exists = self.month_has_data(income_data, month)
            expen_month_data_exists = self.month_has_data(expenses_data, month)

            if income_month_data_exists or expen_month_data_exists:
                print(
                    Fore.GREEN + Style.BRIGHT +
                    f"\nCalculating {month} income and expenses...\n" +
                    Style.RESET_ALL)
                if not income_month_data_exists:
                    print(
                        Fore.YELLOW +
                        f"Warning: NO INCOME data found for {month}!\n" +
                        Style.RESET_ALL)
                    total_month_income = 0
                    formatted_income = self.format_amount_for_display(
                        total_month_income)
                else:
                    total_month_income = self.calculate_total_amount(
                        income_data, month, 2)
                    # Show the income in European currency format
                    formatted_income = self.format_amount_for_display(
                        total_month_income)
                if not expen_month_data_exists:
                    print(
                        Fore.YELLOW +
                        f"Warning: NO EXPENSES data found for {month}!\n" +
                        Style.RESET_ALL)
                    total_month_expenses = 0
                    formatted_expenses = self.format_amount_for_display(
                        total_month_expenses)
                else:
                    total_month_expenses = self.calculate_total_amount(
                        expenses_data, month, 3)
                    # Show the expenses in European currency format
                    formatted_expenses = self.format_amount_for_display(
                        total_month_expenses)

                print(f"✅ AGGREGATE TOTAL INCOME: {formatted_income} EUR")
                print(f"✅ AGGREGATE TOTAL EXPENSES: {formatted_expenses} EUR\n")

                # Calculate net financial balance
                print(
                    Fore.GREEN + Style.BRIGHT +
                    f"\nCalculating net financial balance for {month}\n" +
                    Style.RESET_ALL
                    )
                balance = total_month_income - total_month_expenses
                formatted_balance = self.format_amount_for_display(balance)

                if balance >= 0:
                    print(f"🎉🎉 Positive Balance!: {formatted_balance} EUR\n")
                else:
                    print(f"🚨🚨 Negative Balance!: {formatted_balance} EUR\n")

                self.show_monthly_expenses_details(month)

                prompt_for_menu_or_exit()

            else:
                print(f"""
                {Fore.LIGHTRED_EX}\nThere is no data for {month} yet...
                {Style.RESET_ALL}"
                """)
                prompt_for_menu_or_exit()


def validate_user_numbers_choice(user_input):
    """Validates the user's choice."""
    if not 0 <= user_input <= 4:
        raise ValueError(
            Fore.LIGHTRED_EX +
            "Invalid input: Please enter a number (0-4) or E.\n" +
            Style.RESET_ALL)


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
        finance_manager.display_worksheet("incomes")
        finance_manager.display_worksheet("expenses")
        prompt_for_menu_or_exit()

    elif option == 4:
        return finance_manager.generate_monthly_finance_report()


def get_menu_user_choice():
    """Gets the user's choice from the menu options."""
    while True:
        print(f"""
    {Fore.GREEN + Style.BRIGHT}==== MENU OPTIONS ===={Style.RESET_ALL}

    Press 0 to check the application instructions.
    Press 1 to add a new income entry (Month, Source, and Amount).
    Press 2 to add a new expense entry (Month, Category, Description, Amount).
    Press 3 to view all incomes and expenses.
    Press 4 to view AGGREGATED 2025 MONTHLY FINANCE REPORT.
    Press E to exit the program.
        """)

        try:
            choice_message = (
                Fore.BLUE + Style.BRIGHT +
                "\nEnter your choice (0-4 or E) and press enter:\n" +
                Style.RESET_ALL
            )
            user_input = input(choice_message).strip().upper()

            if user_input == "E":
                return exit_program()

            # Check for empty input
            if not user_input:
                raise ValueError(
                    Fore.LIGHTRED_EX +
                    "Empty input: Please enter a number (0-4) or E.\n" +
                    Style.RESET_ALL
                )
            # Check if input looks like a number
            if not is_valid_number(user_input):
                raise ValueError(
                    Fore.LIGHTRED_EX +
                    "Invalid input: Please enter a number (0-4) or E.\n" +
                    Style.RESET_ALL
                )
            # Convert user input to integer
            option = int(user_input)

            validate_user_numbers_choice(option)
            return handle_user_option(option)

        except ValueError as error:
            print(error)


def main():
    """
    Initializes the application, displays the welcome message, 
    and starts the main menu loop.
    """
    welcome()
    get_menu_user_choice()


main()
