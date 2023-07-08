import pandas as pd
import matplotlib.pyplot as plt
from pySankey.sankey import sankey

df = pd.read_csv("WorldCruiseData.csv", sep=",")

# Create Sankey diagram again
sankey(
    left=df["INCOME"], right=df["EXPENSES"], 
    leftWeight= df["PRICE"], rightWeight=df["PRICE"], 
    aspect=20, fontsize=20
)

# Get current figure
fig = plt.gcf()

# Set size in inches
fig.set_size_inches(6, 6)

# Set the color of the background to white
fig.set_facecolor("w")

# Save the figure
fig.savefig("customers-goods.png", bbox_inches="tight", dpi=150)