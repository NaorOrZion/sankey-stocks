# Sankey Stocks

Author: Naor Or-Zion

## What is the _Sankey Stocks_ program?

Welcome to the Sankey-Stocks program!
This tool has been crafted to enable users of all ages, even 10-year-old enthusiasts, to effortlessly visualize income statements. The annual data is sourced from "https://site.financialmodelingprep.com/" so make sure to sign up on the website to obtain your API key.

You can input the API key directly into the designated variable (named "API_KEY", found in sankey-stocks.py file) after reviewing the instructions, or opt for a more secure approach by retrieving it through an environment variable.

Explore the API documentation at "https://site.financialmodelingprep.com/developer/docs/" for a comprehensive understanding. Additionally, delve into Plotly's chart documentation at "https://plotly.com/python/sankey-diagram/" to unlock the full potential of dynamic visualizations.

**Before**: An ugly income statement that is hard to read.

[![Income-Statement](https://miro.medium.com/v2/resize:fit:720/format:webp/1*Q1NGoe-1JpOBhYHku_3Sww.png)](https://medium.com/@javierlangarica/the-income-statement-3409bd07bc9d)

**After**: An easy to understand sankey chart (2021 Income statement):

[![Income-Statement](https://i.ibb.co/HpQsMd7/Newplot-1.png)](https://ibb.co/jZF2xRh)

**Please notice**
- An optimal sankey chart will be created only when the company is profitable (Net income greater than 0$).
- A chart will be displayed in html page with unordered dynamic nodes that you can drag & drop as you wish.
- Not all companies have a good chart, that's because some of them post their data differently.
- When you are asked to write a ticker, please remember that a ticker is the "name" of the stock and not the name of the company.

## Installation

#### Requirements
- Python 3

Clone the repository from github to a designated folder:

```sh
git clone https://github.com/NaorOrZion/sankey-stocks.git
```

A recommended way is to set up a virtual environment for python, which holds an 
interpreter with all the needed packages:

```sh
cd sankey-stocks
python -m venv venv_folder
```

Activate the new virtual environment venv_folder:

```sh
.\venv_folder\Scripts\activate
```

Download the libraries from the "requirements.txt" file:

```sh
pip install -r requirements.txt
```

#### Run the program

```sh
python sankey-stocks.py
```

You are done!
Now just follow the program.

**Free Software!**