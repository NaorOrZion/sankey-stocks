import plotly.graph_objects as go
from numerize import numerize
import re

from income_statement_utils import (create_request, 
                                  get_quarterly_statement_dates_dict, 
                                  get_annualy_statement_dates_dict,
                                  get_income_statement_by_given_date)


"""
This project was designed to visualize a company's income statement in a way that 
even a 10 years old kid could understand it.

Using https://plotly.com/python/sankey-diagram/ for waves documentation.
Using Rapidapi.com for yahoo finance api.
"""

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
       generate a sankey chart of the company's income statement in an HTML page.\n")

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

                quarterly_dates_dict =      get_quarterly_statement_dates_dict(ticker_dict=response_data_dict)
                quarterly_dates_list =      list(quarterly_dates_dict.keys())

                annualy_dates_dict =        get_annualy_statement_dates_dict(ticker_dict=response_data_dict)
                annualy_dates_list =        list(annualy_dates_dict.keys())

                quarterly_dates_dict.update(annualy_dates_dict)
                total_dates_dict =          quarterly_dates_dict
                total_dates_list =          quarterly_dates_list + annualy_dates_list
                dates_index =               1

                # Print quarterly dates options
                print("\nQuarterly dates:")
                for index_q in range(len(quarterly_dates_list)):
                    print(f"{dates_index}. {quarterly_dates_list[index_q]}")
                    dates_index += 1

                # Print annualy dates options
                print("\nAnnualy dates:")
                for index_a in range(len(annualy_dates_list)):
                    print(f"{dates_index}. {annualy_dates_list[index_a]}")
                    dates_index += 1
                
                # Check whether the user's choice is valid - if not, repeat loop.
                user_report_choice = is_report_choice_valid(index=dates_index)
                if user_report_choice is False: continue

                # Store the ticker dictionary with all it's data according to user's choice.
                report_date = total_dates_list[user_report_choice - 1]
                ticker_dict = total_dates_dict[report_date]

                # Create a dictionary called "links" - to attach a values to their title.
                links = create_links_dict(ticker_dict=ticker_dict)

                links_index = list(links)
                link = lambda key: links_index.index(key)

                SOURCE = [
                    link("REVENUE"),                    # - > GROSS_PROFIT
                    link("GROSS_PROFIT"),               # - > OPERATING_INCOME
                    link("OPERATING_INCOME"),           # - > NET_INCOME
                    link("OPERATING_INCOME"),           # - > TAX_ON_OPERATING_INCOME   
                    link("OPERATING_INCOME"),           # - > TOTAL_OTHER_INCOME_EXPENSES_NET    
                    link("GROSS_PROFIT"),               # - > OPERATING_EXPENSES
                    link("OPERATING_EXPENSES"),         # - > R_N_D_EXPENSES      
                    link("OPERATING_EXPENSES"),         # - > SELL_GEN_ADMIN_EXPENSES      
                    link("OPERATING_EXPENSES"),         # - > OTHER_OPERATING_EXPENSES     
                    link("REVENUE")                     # - > COST_OF_REVENUE
                ]
                
                TARGET = [
                    link("GROSS_PROFIT"),
                    link("OPERATING_INCOME"), 
                    link("NET_INCOME"), 
                    link("TAX_ON_OPERATING_INCOME"), 
                    link("TOTAL_OTHER_INCOME_EXPENSES_NET"), 
                    link("OPERATING_EXPENSES"), 
                    link("R_N_D_EXPENSES"), 
                    link("SELL_GEN_ADMIN_EXPENSES"), 
                    link("OTHER_OPERATING_EXPENSES"),
                    link("COST_OF_REVENUE")
                ]

                fig = go.Figure(data=[go.Sankey(
                node = dict(
                pad = 80,
                thickness = 70,
                label = [
                        f"Revenue\n{links['REVENUE']['fmt']}", 
                        f"Gross Profit\n{links['GROSS_PROFIT']['fmt']}",
                        f"Cost of Revenue\n{links['COST_OF_REVENUE']['fmt']}", 

                        f"Operating Expenses\n{links['OPERATING_EXPENSES']['fmt']}", 
                        f"Research & \nDevelopment\n{links['R_N_D_EXPENSES']['fmt']}", 
                        f"Selling & \nGeneral &\nAdmin\n{links['SELL_GEN_ADMIN_EXPENSES']['fmt']}", 
                        f"Other\n{links['OTHER_OPERATING_EXPENSES']['fmt'] if links['OTHER_OPERATING_EXPENSES'] else '0'}", 
                        
                        f"Operating Income\n{links['OPERATING_INCOME']['fmt']}", 
                        f"Tax\n{links['TAX_ON_OPERATING_INCOME']['fmt']}", 
                        f"Net Income\n{links['NET_INCOME']['fmt']}", 
                        f"Other Income Expenses\n{links['TOTAL_OTHER_INCOME_EXPENSES_NET']['fmt']}" 
                        ],

                color = [RED_BAR if bar in [2, 3, 4, 5, 7, 9] else GREEN_BAR \
                        if bar != 0 else BLUE_BAR for bar in set(SOURCE + TARGET)]),
                link = dict(
                    source = SOURCE,
                    target = TARGET,
                    value =  [
                            links['GROSS_PROFIT']['raw'],              
                            links['OPERATING_INCOME']['raw'],          
                            links['NET_INCOME']['raw'],                
                            abs(links['TAX_ON_OPERATING_INCOME']['raw']),       
                            links['TOTAL_OTHER_INCOME_EXPENSES_NET']['raw'],       
                            links['OPERATING_EXPENSES']['raw'],          
                            links['R_N_D_EXPENSES']['raw'],                      
                            links['SELL_GEN_ADMIN_EXPENSES']['raw'],                                    
                            (links['OTHER_OPERATING_EXPENSES']['raw'] if links['OTHER_OPERATING_EXPENSES'] else 0),            
                            links['COST_OF_REVENUE']['raw']                          
                            ],                                      
                    color=[RED_WAVE if target in [2, 3, 4, 5, 7, 9] else GREEN_WAVE for target in TARGET]
                ))])

            fig.update_layout(title_text=f"{ticker.upper()} Financial statment for {report_date}", font_size=20)
            fig.show()
        else:
            print("Please choose a valid option!\n")
            continue


def is_report_choice_valid(index) -> bool: 
    '''
    This function validates the report number choosen.
    If it's between 0 and the index range, it will return True, elsewise False.
    :params     index -> int
    :returns    bool / number -> int
    '''
    try:
        number = int(input("\nReport number: "))
        if 0 < number < index:
            return number
        else:
            print("\nPlease choose an option from the given list!")
            return False
    except (ValueError, TypeError):
        print("\nAn error occured, please choose a valid option!")
        return False


def create_links_dict(ticker_dict):
    '''
    This function is responsible for the links creation.
    It means to create a dictionary that match every element in the ticker_dict to its value ("'REVENUE': 100,000").
    :params     ticker_dict -> Dict[str, Dict]
    :returns    links       -> Dict[str, int]
    '''
    links = {
        "REVENUE":                          ticker_dict['totalRevenue'],
        "GROSS_PROFIT":                     ticker_dict['grossProfit'],
        "COST_OF_REVENUE":                  ticker_dict['costOfRevenue'],

        "OPERATING_EXPENSES":               ticker_dict['totalOperatingExpenses'],
        "R_N_D_EXPENSES":                   ticker_dict['researchDevelopment'],
        "SELL_GEN_ADMIN_EXPENSES":          ticker_dict['sellingGeneralAdministrative'],
        "OTHER_OPERATING_EXPENSES":         ticker_dict['otherOperatingExpenses'],

        "OPERATING_INCOME":                 ticker_dict['operatingIncome'],
        "TAX_ON_OPERATING_INCOME":          ticker_dict['incomeTaxExpense'],
        "NET_INCOME":                       ticker_dict['netIncome'],
        "TOTAL_OTHER_INCOME_EXPENSES_NET":  ticker_dict['totalOtherIncomeExpenseNet']
    }

    return links


if __name__ == "__main__":
    handle_usr_input()