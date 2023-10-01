import plotly.graph_objects as go
from numerize import numerize
import requests
import re


"""
  Welcome to the sankey-stocks program!
  This program was written in order for the user to visualize an income statement even if the user is a 10 years old kid.
  The income statements are annualy (yearly) and are taken from the website "https://site.financialmodelingprep.com/".
  Please create a user in this website in order to get an API key.
  Paste the API key as a string in first variable after reading the explanation or retrieve it by using an evironment variable (safer).

  To the API documentation: "https://site.financialmodelingprep.com/developer/docs/".
  To the plotly charts documentation: "https://plotly.com/python/sankey-diagram/".

  Author: Naor Or-Zion
"""

# Api key
API_KEY = ""

# Settings Consts
TICKER_PATTERN = '([A-Za-z]{1,5})(-[A-Za-z]{1,2})?'

# Colors Consts
RED_WAVE = "#EDA19B"
RED_BAR = "#DB4437"

GREEN_WAVE = "#87CEAB"
GREEN_BAR =  "#0F9D58"

BLUE_WAVE = "#A0C2F9"
BLUE_BAR = "#4285F4"


def handle_user_input():
  """
    Handle user input, create sankey-chart accordingly.
  """
  while True:
    print("\nWhat would you like to do?")
    print("1. Create a sankey chart")
    print("2. exit")

    option = input("\nOption: ")

    if option == '2':
      break

    elif option == '1':
      ticker = input("Please enter a ticker: ")
      is_ticker_valid = re.fullmatch(TICKER_PATTERN, ticker)

    else:
      print("Please choose a valid option!\n")
      continue

    if not is_ticker_valid:
      print("Not a valid ticker. A ticker should look like this: 'AAPL' or 'TSLA'")
      continue

    # Retrieve income statement data
    income_statement_data = get_income_statement_data(ticker=ticker)
    if not income_statement_data: continue
    
    # Print the options of the last 4 years of company's income statement
    print("\nWhich annual year would like to view?")
    for index, data in enumerate(income_statement_data):
      print(f"{index + 1}. {data['date']}")
    
    # User annual year preference
    date_picked = int(input("Option: ")) - 1

    # Get the data for the sankey chart.
    source, target, links = get_sankey_chart_data(income_statement_data=income_statement_data[date_picked])

    # Create a figure
    fig = get_figure(values_dict=links, source=source, target=target)

    # Get the date from the income_statement_data.
    date_link = income_statement_data[date_picked]['date']

    # Display the title of the html page.
    fig.update_layout(title_text=f"{ticker.upper()} Annual financial statment for {date_link}", font_size=20)

    # Initialize the sankey chart.
    fig.show()


def get_figure(values_dict, source, target):
  """
    This funciton creates a figure by the giving data.
    It needs a list of source indexes and target indexes.
    Every source is a block/node just like a target.
    The values_dict is a dictionary indicating what is the value for every node or wave.
    @params:  values_dict  -> Dict[str, int]
              source -> List[int]
              target -> List[int]
    Returns:  fig    -> Fig Object
  """
  # Create a list out of the dictionary.
  values_index = list(values_dict)

  # Create a lambda function to retrieve a key's index by a key's value.
  value = lambda key: values_index.index(key)

  fig = go.Figure(data=[go.Sankey(
          node = dict(
          pad = 80,
          thickness = 70,
          label = [
                    f"Revenue\n{numerize.numerize(values_dict['REVENUE'])}", 
                    f"Gross Profit\n{numerize.numerize(values_dict['GROSS_PROFIT'])}",
                    f"Cost of Revenue\n{numerize.numerize(values_dict['COST_OF_REVENUE'])}", 

                    f"Operating Expenses\n{numerize.numerize(values_dict['OPERATING_EXPENSES'])}", 
                    f"Research & \nDevelopment\n{numerize.numerize(values_dict['R_N_D_EXPENSES'])}", 
                    f"Selling & \nGeneral &\nAdmin\n{numerize.numerize(values_dict['SELL_GEN_ADMIN_EXPENSES'])}", 
                    f"General & \nAdministrative\n{numerize.numerize(values_dict['GEN_ADMIN_EXPENSES'])}", 
                    f"Selling & \nMarketing\n{numerize.numerize(values_dict['SELL_MARKETING_EXPENSES'])}", 
                    f"Other\n{numerize.numerize(values_dict['OTHER_OPERATING_EXPENSES'])}", 
                    
                    f"Operating Income\n{numerize.numerize(values_dict['OPERATING_INCOME'])}", 
                    f"Tax\n{numerize.numerize(values_dict['TAX_ON_OPERATING_INCOME'])}", 
                    f"Net Income\n{numerize.numerize(values_dict['NET_INCOME'])}", 
                    f"Other Income Expenses\n{numerize.numerize(abs(values_dict['TOTAL_OTHER_INCOME_EXPENSES_NET']))}" 
                    ],
          color = [RED_BAR if bar in 
                   [value('COST_OF_REVENUE'), 
                    value('OPERATING_EXPENSES'), 
                    value('R_N_D_EXPENSES'), 
                    value('SELL_GEN_ADMIN_EXPENSES'), 
                    value('GEN_ADMIN_EXPENSES'), 
                    value('SELL_MARKETING_EXPENSES'), 
                    value('OTHER_OPERATING_EXPENSES'), 
                    value('TAX_ON_OPERATING_INCOME'), 
                    value('TOTAL_OTHER_INCOME_EXPENSES_NET'), 
                  ] \
                   else GREEN_BAR if bar != 0 else BLUE_BAR for bar in set(source + target)]
        ),
        link = dict(
          source = source,
          target = target,
          value =  [
                    values_dict['GROSS_PROFIT'],              
                    values_dict['OPERATING_INCOME'],          
                    values_dict['NET_INCOME'],                
                    values_dict['TAX_ON_OPERATING_INCOME'],       
                    values_dict['TOTAL_OTHER_INCOME_EXPENSES_NET'],       
                    values_dict['OPERATING_EXPENSES'],          
                    values_dict['R_N_D_EXPENSES'],                      
                    values_dict['SELL_GEN_ADMIN_EXPENSES'],               
                    values_dict['GEN_ADMIN_EXPENSES'],                    
                    values_dict['SELL_MARKETING_EXPENSES'],                       
                    values_dict['OTHER_OPERATING_EXPENSES'],            
                    values_dict['COST_OF_REVENUE']                          
          ],                                      
          color=[RED_WAVE if target in [2, 3, 4, 5, 6, 7, 8, 10, 12] else GREEN_WAVE for target in target]
      ))])

  return fig

def get_sankey_chart_data(income_statement_data):
  """
    Create data such as source nodes and target nodes indexes so we can use later to create the sankey chart.
    Additionally, create a dictionary that stores the value of each block to be used later in the sankey chart.
    @params:  income_statement_data -> Dict[str, str/int]
    Returns:  source                -> List[int]
              target                -> List[int]
              links                 -> Dict[str, int]
  """

  links = {
    "REVENUE": income_statement_data["revenue"],
    "GROSS_PROFIT": income_statement_data["grossProfit"],
    "COST_OF_REVENUE": income_statement_data["costOfRevenue"],

    "OPERATING_EXPENSES": income_statement_data["operatingExpenses"],
    "R_N_D_EXPENSES": income_statement_data["researchAndDevelopmentExpenses"],
    "SELL_GEN_ADMIN_EXPENSES": income_statement_data["sellingGeneralAndAdministrativeExpenses"],
    "GEN_ADMIN_EXPENSES": income_statement_data["generalAndAdministrativeExpenses"],
    "SELL_MARKETING_EXPENSES": income_statement_data["sellingAndMarketingExpenses"],
    "OTHER_OPERATING_EXPENSES": income_statement_data["otherExpenses"],

    "OPERATING_INCOME": income_statement_data["operatingIncome"],
    "TAX_ON_OPERATING_INCOME": income_statement_data["incomeTaxExpense"],
    "NET_INCOME": income_statement_data["netIncome"],
    "TOTAL_OTHER_INCOME_EXPENSES_NET": abs(income_statement_data["totalOtherIncomeExpensesNet"])
  }

  # Create a list out of the dictionary.
  links_index = list(links)

  # Create a lambda function to retrieve a key's index by a key's value.
  link = lambda key: links_index.index(key)

  # The source and target should be a list of indexes ([0, 1, 4, 3....]). 
  # An index will point to another index. 
  # Later on we will use the values from the "links" dictionary to pair those indexes to their values, by so creating a wave and blocks.
  source = [
    link("REVENUE"),                  # - > GROSS_PROFIT
    link("GROSS_PROFIT"),             # - > OPERATING_INCOME
    link("OPERATING_INCOME"),         # - > NET_INCOME
    link("OPERATING_INCOME"),         # - > TAX_ON_OPERATING_INCOME
    link("OPERATING_INCOME"),         # - > TOTAL_OTHER_INCOME_EXPENSES_NET
    link("GROSS_PROFIT"),             # - > OPERATING_EXPENSES
    link("OPERATING_EXPENSES"),       # - > R_N_D_EXPENSES
    link("OPERATING_EXPENSES"),       # - > SELL_GEN_ADMIN_EXPENSES
    link("SELL_GEN_ADMIN_EXPENSES"),  # - > GEN_ADMIN_EXPENSES
    link("SELL_GEN_ADMIN_EXPENSES"),  # - > SELL_MARKETING_EXPENSES
    link("OPERATING_EXPENSES"),       # - > OTHER_OPERATING_EXPENSES
    link("REVENUE")                   # - > COST_OF_REVENUE
  ]

  target = [
    link("GROSS_PROFIT"),
    link("OPERATING_INCOME"),
    link("NET_INCOME"),
    link("TAX_ON_OPERATING_INCOME"),
    link("TOTAL_OTHER_INCOME_EXPENSES_NET"),
    link("OPERATING_EXPENSES"),
    link("R_N_D_EXPENSES"),
    link("SELL_GEN_ADMIN_EXPENSES"),
    link("GEN_ADMIN_EXPENSES"),
    link("SELL_MARKETING_EXPENSES"),
    link("OTHER_OPERATING_EXPENSES"),
    link("COST_OF_REVENUE")
  ]

  return source, target, links


def get_income_statement_data(ticker):
  """
    Gets the income statement data for the given ticker from the Financial Modeling Prep API.
    @params:  ticker        -> str,
              api_key       -> str.
    Return:   response_data -> Dict[str, int]
  """
  response = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=120&apikey={API_KEY}")
  response_data = response.json()

  if "Error Message" in response_data:
    print("Error making the request:", response_data["Error Message"])
    return None

  if not response_data:
    print("Error making the request: The ticker doesn't exists")
    return None

  return response_data


def main():
  """
    The main function.
  """
  print("This is the Sankey-Stock program!")
  print("The program gets a ticker for input, and generate a sankey chart of\n \
        the company's chosen annual income statement in HTML.\n")
  handle_user_input()
  

if __name__ == "__main__":
  main()