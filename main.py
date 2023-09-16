import plotly.graph_objects as go
from numerize import numerize
import requests
import re

from income_statement_utils import (create_request, 
                                  get_quarterly_statement_dates_list, 
                                  get_annualy_statement_dates_list)


"""
  # Using https://plotly.com/python/sankey-diagram/ for documentation

     המספרים במקור וביעד הם מספרים שמציינים את המיקום של איברים במשתנה
       label
"""

# Api key
API_KEY = "6b99cdd3620bba8d52b849d9a1fab7e4"

# Settings Consts
TICKER_PATTERN = '([A-Za-z]{1,5})(-[A-Za-z]{1,2})?'
VALID_REGIONS = ["US", "BR", "AU", "CA", "FR", "DE", "HK", "IN", "IT", "ES", "GB", "SG"]

# Colors Consts
RED_WAVE = "#EDA19B"
RED_BAR = "#DB4437"

GREEN_WAVE = "#87CEAB"
GREEN_BAR =  "#0F9D58"

BLUE_WAVE = "#A0C2F9"
BLUE_BAR = "#4285F4"

print("This is the Sankey-Stock program!")
print("In this program you can enter a ticker, and the program will\n \
       generate a sankey chart of the company's last annual balance sheet in HTML\n")

def handle_usr_input():
    while True:
        print("\nWhat would you like to do?")
        print("1. Create a sankey chart")
        print("2. exit")

        option = input("\nOption: ")

        if option == '2':
            break

        if option == '1':
            # Validate ticker input
            ticker = input("Please enter a ticker: ")
            is_ticker_valid = re.fullmatch(TICKER_PATTERN, ticker)

            # Validate region input
            region = input("\nPlease enter ticker's region.\nOnly one of the following is allowed:\nUS|BR|AU|CA|FR|DE|HK|IN|IT|ES|GB|SG: ")
            region = region.upper()
            is_region_valid = True if region in VALID_REGIONS else False

            if is_ticker_valid and is_region_valid:
                response_data_dict = create_request(ticker, region)

                if not response_data_dict:
                    print("\nError making the request: This ticker does not exists.")
                    continue
                
                print("\n======================================")
                print("\nWhich report would you like to view?")

                quarterly_dates = get_quarterly_statement_dates_list(ticker_dict=response_data_dict)
                annual_dates = get_annualy_statement_dates_list(ticker_dict=response_data_dict)
                dates_index = 1

                print("\nQuarterly dates:")
                for index_q in range(len(quarterly_dates)):
                    print(f"{dates_index}. {quarterly_dates[index_q]}")
                    dates_index += 1

                print("\nAnnualy dates:")
                for index_a in range(len(annual_dates)):
                    print(f"{dates_index}. {annual_dates[index_a]}")
                    dates_index += 1
                
                user_report_choice = is_report_choice_valid(index=dates_index)
                if user_report_choice is False: continue
                    
        else:
            print("Please choose a valid option!\n")
            continue


def is_report_choice_valid(index) -> bool: 
    '''
    This function validates the report number choosen.
    If it's between 0 and the index range, it will return True, elsewise False.
    :params     index -> int
    :returns    bool / number -> str
    '''
    try:
        number = int(input("\nReport number: "))
        if 0 < number < index:
            return str(number)
        else:
            print("\nPlease choose an option from the given list!")
            return False
    except (ValueError, TypeError):
        print("\nAn error occured, please choose a valid option!")
        return False


if __name__ == "__main__":
    handle_usr_input()