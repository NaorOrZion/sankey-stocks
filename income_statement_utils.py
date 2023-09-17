import requests
from typing import List, Dict

RAPIDAPI_API_KEY = "0c2ac85f22mshebe80e1a88ac076p1a5357jsn9a48d9493f09"
RAPIDAPI_HOST = "apidojo-yahoo-finance-v1.p.rapidapi.com"
REQUEST_URL = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-financials"

def create_request(symbol, region="US") -> Dict[str, Dict]:
    '''
    This function creates a request to rapidapi.com with an API key in order
    to retrieve a company financials.
    It returns a dictionary full of financial data.
    :params symbol (a company ticker)   -> str,
            region (a company's region) -> str
    :returns ticker_dict -> Dict[str, Dict]
    '''
    querystring = {"symbol": symbol,"region": region}

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_API_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    response = requests.get(REQUEST_URL, headers=headers, params=querystring)
    ticker_dict = response.json()

    return ticker_dict


def get_quarterly_statement_dates_dict(ticker_dict) -> Dict[str, Dict]:
    '''
    This function gets a ticker's dictionary of a company as a parameter, and returns
    a dictionary of the last quarterly statement dates as a key, and their data as a value.
    :params     ticker_dict     -> dict
    :returns    quarterly_dates -> Dict[str, Dict]
    '''
    quarterly_dates = {}

    for statement in ticker_dict["incomeStatementHistoryQuarterly"]["incomeStatementHistory"]:
        quarterly_dates[statement["endDate"]["fmt"]] = statement

    return quarterly_dates


def get_annualy_statement_dates_dict(ticker_dict) -> Dict[str, Dict]:
    '''
    This function gets a ticker's dictionary of a company as a parameter, and returns
    a dictionary of the last annualy statement dates as a key, and their data as a value.
    :params     ticker_dict     -> dict
    :returns    annualy_dates   -> Dict[str, Dict]
    '''
    annualy_dates = {}

    for statement in ticker_dict["incomeStatementHistory"]["incomeStatementHistory"]:
        annualy_dates[statement["endDate"]["fmt"]] = statement

    return annualy_dates


def get_income_statement_by_given_date(ticker_dict, date):
    '''
    This function will retrieve an income statement from the ticker_dict by a given date.
    :params     ticker_dict         -> Dict[str, Dict]
                date                -> str (format: YYYY-MM-DD)
    :returns    income_statement    -> Dict[str, Dict]
    '''
    pass
