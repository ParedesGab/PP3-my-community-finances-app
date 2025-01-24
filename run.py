import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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

#Access my-finances worksheet
income = SHEET.worksheet('income')
expenses = SHEET.worksheet("expenses")

income_data = income.get_all_values()
expenses_data = expenses.get_all_values()

pprint(income_data) #output: a list of rows with string values
pprint(expenses_data) #output: a list of rows with string values