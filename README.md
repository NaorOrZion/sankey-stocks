# Sankey Stocks

Author: Naor Or-Zion

## What is the _Sankey Stocks_ program?

Welcome to the Sankey-Stocks program!
This tool has been crafted to enable users of all ages, even 10-year-old enthusiasts, to effortlessly visualize income statements. The annual data is sourced from "https://site.financialmodelingprep.com/" so make sure to sign up on the website to obtain your API key.

You can input the API key directly into the designated variable after reviewing the instructions, or opt for a more secure approach by retrieving it through an environment variable.

Explore the API documentation at "https://site.financialmodelingprep.com/developer/docs/" for a comprehensive understanding. Additionally, delve into Plotly's chart documentation at "https://plotly.com/python/sankey-diagram/" to unlock the full potential of dynamic visualizations.

**Before**: An ugly income statement that is hard to read.

[![Income-Statement](https://miro.medium.com/v2/resize:fit:720/format:webp/1*Q1NGoe-1JpOBhYHku_3Sww.png)](https://medium.com/@javierlangarica/the-income-statement-3409bd07bc9d)

**After**: An easy to understand sankey chart (2021 Income statement):

[![Income-Statement](https://i.ibb.co/HpQsMd7/Newplot-1.png)](https://ibb.co/jZF2xRh)

**Please notice**
- An optimal sankey chart will be created only when the company is profitable.
- A chart will be displayed in html page with unordered dynamic nodes that you can drag & drop as you wish.
- Not all companies have a good chart, that's because some of them post their data differently.
