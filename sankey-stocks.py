import plotly.graph_objects as go
from numerize import numerize
import requests
import re


"""
  # Using https://plotly.com/python/sankey-diagram/ for documentation

     המספרים במקור וביעד הם מספרים שמציינים את המיקום של איברים במשתנה
       label
"""

# Api key
API_KEY = "6b99cdd3620bba8d52b849d9a1fab7e4"

# Settings Consts
TICKER_PATTERN = '([A-Za-z]{1,5})(-[A-Za-z]{1,2})?'

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

while True:
  print("\nWhat would you like to do?")
  print("1. Create a sankey chart")
  print("2. exit")

  option = input("\nOption: ")

  if option == '2':
    break

  if option == '1':
    ticker = input("Please enter a ticker: ")
    is_ticker_valid = re.fullmatch(TICKER_PATTERN, ticker)

    if is_ticker_valid:
      response = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=120&apikey={API_KEY}")
      response_data = response.json()
      if "Error Message" in response_data:
        print("Error making the request:", response_data["Error Message"])
        continue

      if not response_data:
         print("Error making the request: The ticker doesn't exists")
         continue
      
      print("\nWhich annual year would like to view?")
      for index, data in enumerate(response_data):
        print(f"{index + 1}. {data['date']}")
      
      date_picked = int(input("Option: ")) - 1
      
      date_link = response_data[date_picked]['date']

      links = {
        "REVENUE":                          response_data[date_picked]['revenue'],
        "GROSS_PROFIT":                     response_data[date_picked]['grossProfit'],
        "COST_OF_REVENUE":                  response_data[date_picked]['costOfRevenue'],

        "OPERATING_EXPENSES":               response_data[date_picked]['operatingExpenses'],
        "R_N_D_EXPENSES":                   response_data[date_picked]['researchAndDevelopmentExpenses'],
        "SELL_GEN_ADMIN_EXPENSES":          response_data[date_picked]['sellingGeneralAndAdministrativeExpenses'],
        "GEN_ADMIN_EXPENSES":               response_data[date_picked]['generalAndAdministrativeExpenses'],
        "SELL_MARKETING_EXPENSES":          response_data[date_picked]['sellingAndMarketingExpenses'],
        "OTHER_OPERATING_EXPENSES":         response_data[date_picked]['otherExpenses'],

        "OPERATING_INCOME":                 response_data[date_picked]['operatingIncome'],
        "TAX_ON_OPERATING_INCOME":          response_data[date_picked]['incomeTaxExpense'],
        "NET_INCOME":                       response_data[date_picked]['netIncome'],
        "TOTAL_OTHER_INCOME_EXPENSES_NET":  abs(response_data[date_picked]['totalOtherIncomeExpensesNet'])
      }

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
                link("SELL_GEN_ADMIN_EXPENSES"),    # - > GEN_ADMIN_EXPENSES      
                link("SELL_GEN_ADMIN_EXPENSES"),    # - > SELL_MARKETING_EXPENSES      
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
                link("GEN_ADMIN_EXPENSES"), 
                link("SELL_MARKETING_EXPENSES"), 
                link("OTHER_OPERATING_EXPENSES"),
                link("COST_OF_REVENUE")
            ]

      fig = go.Figure(data=[go.Sankey(
            node = dict(
            pad = 80,
            thickness = 70,
            label = [
                     f"Revenue\n{numerize.numerize(links['REVENUE'])}", 
                     f"Gross Profit\n{numerize.numerize(links['GROSS_PROFIT'])}",
                     f"Cost of Revenue\n{numerize.numerize(links['COST_OF_REVENUE'])}", 

                     f"Operating Expenses\n{numerize.numerize(links['OPERATING_EXPENSES'])}", 
                     f"Research & \nDevelopment\n{numerize.numerize(links['R_N_D_EXPENSES'])}", 
                     f"Selling & \nGeneral &\nAdmin\n{numerize.numerize(links['SELL_GEN_ADMIN_EXPENSES'])}", 
                     f"General & \nAdministrative\n{numerize.numerize(links['GEN_ADMIN_EXPENSES'])}", 
                     f"Selling & \nMarketing\n{numerize.numerize(links['SELL_MARKETING_EXPENSES'])}", 
                     f"Other\n{numerize.numerize(links['OTHER_OPERATING_EXPENSES'])}", 
                     
                     f"Operating Income\n{numerize.numerize(links['OPERATING_INCOME'])}", 
                     f"Tax\n{numerize.numerize(links['TAX_ON_OPERATING_INCOME'])}", 
                     f"Net Income\n{numerize.numerize(links['NET_INCOME'])}", 
                     f"Other Income Expenses\n{numerize.numerize(abs(links['TOTAL_OTHER_INCOME_EXPENSES_NET']))}" 
                     ],
            color = [RED_BAR if bar in [2, 3, 4, 5, 6, 7, 8, 10, 12] else GREEN_BAR \
                     if bar != 0 else BLUE_BAR for bar in set(SOURCE + TARGET)]
          ),
          link = dict(
            source = SOURCE,
            target = TARGET,
            value =  [
                      links['GROSS_PROFIT'],              
                      links['OPERATING_INCOME'],          
                      links['NET_INCOME'],                
                      links['TAX_ON_OPERATING_INCOME'],       
                      links['TOTAL_OTHER_INCOME_EXPENSES_NET'],       
                      links['OPERATING_EXPENSES'],          
                      links['R_N_D_EXPENSES'],                      
                      links['SELL_GEN_ADMIN_EXPENSES'],               
                      links['GEN_ADMIN_EXPENSES'],                    
                      links['SELL_MARKETING_EXPENSES'],                       
                      links['OTHER_OPERATING_EXPENSES'],            
                      links['COST_OF_REVENUE']                          
                      ],                                      
            color=[RED_WAVE if target in [2, 3, 4, 5, 6, 7, 8, 10, 12] else GREEN_WAVE for target in TARGET]
        ))])

      fig.update_layout(title_text=f"{ticker.upper()} Annual financial statment for {date_link}", font_size=20)
      fig.show()
    else:
      print("Not a valid ticker. A ticker should look like this: 'AAPL' or 'TSLA'")
  else:
    print("Please choose a valid option!\n")
    continue