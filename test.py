from sec_api import XbrlApi
import json

xbrlApi = XbrlApi("b0c3991d0ba4152651efc945b0f0d1220cc38ed993360b95e04d238eb968b825")

# 10-K HTM File URL example
xbrl_json = xbrlApi.xbrl_to_json(
    htm_url="https://www.sec.gov/Archives/edgar/data/320193/000032019320000096/aapl-20200926.htm"
)

# access income statement, balance sheet and cash flow statement
print(xbrl_json["StatementsOfIncome"])
print(xbrl_json["BalanceSheets"])
print(xbrl_json["StatementsOfCashFlows"])

# 10-K XBRL File URL example
xbrl_json = xbrlApi.xbrl_to_json(
    xbrl_url="https://www.sec.gov/Archives/edgar/data/1318605/000156459021004599/tsla-10k_20201231_htm.xml"
)

# 10-K accession number example
xbrl_json = xbrlApi.xbrl_to_json(accession_no="0001564590-21-004599")
with open("text.txt", "w") as f:
    f.write(json.dumps(xbrl_json))