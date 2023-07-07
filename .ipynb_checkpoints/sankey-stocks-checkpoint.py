import pandas as pd
from floweaver import *

"""
floWeaver uses different columns for different purposes based on their names.
Specifically,

source:         specifies where the flow starts
target:         specifies where the flow ends
type:           specifies the type of the flow
value:          specifies the flow rate

Thus, we will rename some columns so that they fit floWeaver’s format.
We will use:

EMBARK_PORT:    as source
DISEMBARK_PORT: as target
CRUISE_REGION:  as type
PRICE_PAID:     as value
"""

df = pd.read_csv("WorldCruiseData.csv")

flows = (
    df.groupby(["EMBARK_PORT", "DISEMBARK_PORT", "CRUISE_REGION"])
    .agg({"PRICE_PAID": "mean"})
    .dropna()
    .reset_index()
)

flows = (
    flows.rename(
        columns={
            "EMBARK_PORT": "source",
            "DISEMBARK_PORT": "target",
            "CRUISE_REGION": "type",
            "PRICE_PAID": "value",
        }
    )
)

nodes = {
    "embark_port": ProcessGroup(flows["source"].unique().tolist()),
    "disembark_port": ProcessGroup(flows["target"].unique().tolist()),
}

ordering = [["embark_port"], ["disembark_port"]]
bundles = [Bundle("embark_port", "disembark_port")]
sdd = SankeyDefinition(nodes, bundles, ordering)
weave(sdd, flows).to_widget()