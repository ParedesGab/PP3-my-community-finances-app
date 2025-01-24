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

pprint(income_data[1]) #output: a list of rows with string values
pprint(expenses_data[2]) #output: a list of rows with string values


#Welcome message

#Ask user to chooce betweeen options
    #if Option1: Check My Finance Report! 
    #elif Option2: Add new income?
    #elif Option3: Add new expense?
    #elif Option4: Exit
    #else choice invalid, print invalid and state what is wrong

#User chose: 1
    #Ask User which month they want to see

    #If choice is invalid: print/raise an error
    #If choice is valid: check if the month has data:

        #No data:
            #print(there is no data for the month yet), only for ABC
            #Ask user: add new income?, add new expense? or Check expenses report for ABC?
        
        # Has data: 
            #Print: calculating your general finances in ABC:
            # ✅ Your total income in ABC was:
            # ✅ Your total expenses in ABC was:

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

        





             


    

