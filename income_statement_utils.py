import requests
from typing import List, Dict

def create_request(symbol, region="US") -> Dict[str, Dict]:
    '''
    This function creates a request to rapidapi.com with an API key in order
    to retrieve a company financials.
    It returns a dictionary full of financial data.
    :params symbol (a company ticker)   -> str,
            region (a company's region) -> str
    :returns ticker_dict -> Dict[str, Dict]
    '''
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-financials"

    querystring = {"symbol": symbol,"region": region}

    headers = {
        "X-RapidAPI-Key": "0c2ac85f22mshebe80e1a88ac076p1a5357jsn9a48d9493f09",
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    ticker_dict = response.json()

    return ticker_dict


def get_quarterly_statement_dates_list(ticker_dict) -> List[str]:
    '''
    This function gets a ticker's dictionary of a company as a parameter, and returns
    a list of the last quarterly statement dates.
    :params     ticker_dict     -> dict
    :returns    quarterly_dates -> List[str]
    '''
    quarterly_dates = []

    for statement in ticker_dict["incomeStatementHistoryQuarterly"]["incomeStatementHistory"]:
        quarterly_dates.append(statement["endDate"]["fmt"])

    return quarterly_dates


def get_annualy_statement_dates_list(ticker_dict) -> List[str]:
    '''
    This function gets a ticker's dictionary of a company as a parameter, and returns
    a list of the last quarterly statement dates.
    :params     ticker_dict     -> dict
    :returns    quarterly_dates -> List[str]
    '''
    annualy_dates = []

    for statement in ticker_dict["incomeStatementHistory"]["incomeStatementHistory"]:
        annualy_dates.append(statement["endDate"]["fmt"])

    return annualy_dates


def get_income_statement_by_given_date(ticker_dict, date):
    '''
    This function will retrieve an income statement from the ticker_dict by a given date.
    :params     ticker_dict         -> Dict[str, Dict]
                date                -> str (format: YYYY-MM-DD)
    :returns    income_statement    -> Dict[str, Dict]
    '''
    pass
