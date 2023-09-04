from math import log
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


markets = pd.read_csv("../datasets/markets_cleaned.csv")
markets.dropna(subset=["months_open"], inplace=True)
markets.drop_duplicates(inplace=True)
markets = markets[~markets.state.isin(["Alaska", "Hawaii"])]
markets["num_items_sold"] = markets.drop(["FMID", "name", "city", "county", "state", "lat", "lon", "months_open"], axis=1).sum(axis=1)

state_population = pd.read_csv("../datasets/census-state-populations.csv")
state_population.columns = ["state", "state_pop"]
markets = pd.merge(markets, state_population, on="state", how="inner")
print(markets)
print(markets.groupby("state").count().sort_values(by="name"))
print(markets.describe(include="all").transpose())

## Is latitude related to months open?
### While exploring the farmers market dataset with a scatter matrix, you noticed a potentially interesting 
### relationship between a market's latitude and the number of months it stays open. Digging into this relationship a 
### bit further, you decide to use Seaborn's regression plot to see if there's any weight to this pattern or if the 
### heavy overlap of the points is playing tricks on your eyes.
### To make the regression line stand out, you'll want to lower the overlapping background points opacity and color 
### them a muted gray. Since you're not going to be making any formal inference and want to quickly investigate a 
### pattern, you can turn off the default uncertainty band.

sns.regplot(
    data=markets, x="lat", y="months_open",
    # Set scatter point opacity & color
    scatter_kws={"alpha": 0.1, "color": "gray"},
    # Disable confidence band
    ci=None
)
plt.show()

## What state is the most market-friendly?
### While exploring the farmer's market data, you wonder what patterns may show up if you aggregated to the state 
### level. Are some states more market-friendly than other states? To investigate this, you group your data by state 
### and get the log-transformed number of markets (log_markets) and state populations (log_pop).

markets_and_pop = (
    markets
    .groupby("state", as_index=False)
    .agg({
       "name": lambda d: log(len(d)),
       "state_pop": lambda d: log(d.iloc[0])
    })
    .rename(columns={
        "name": "log_markets", 
        "state_pop": "log_pop"
    })
)
print(markets_and_pop)

### To visualize, you decide to use a regression plot to get an idea of the 'normal' relationship between market and 
### population numbers and a text-scatter to quickly identify interesting outliers.
g = sns.regplot(
    data=markets_and_pop,
    x="log_markets",
    y="log_pop",
    ci=False,
    # Shrink scatter plot points
    scatter_kws={"s": 2}
)

# Iterate over the rows of the data
for _, row in markets_and_pop.iterrows():
    state, log_market, log_pop = row
    g.annotate(state, (log_market, log_pop), size=10)

plt.show()

## Popularity of goods sold by state
### The farmer's market dataset contains columns corresponding to 28 different goods and whether or not they are sold 
### at that market. You're curious to see if there are any interesting stories in this dataset regarding how likely 
### you are to find a given good at a state's markets. To answer this question, you collapse the data into three 
### columns:

### state - the name of the state
### good - the good of interest
### prop_selling - the proportion of markets in that state that sell that good

markets_goods = markets.drop(["FMID", "name", "city", "county", "lat", "lon", "months_open", "num_items_sold", "state_pop"], axis=1)
goods_by_state = markets_goods.groupby("state", as_index=False).agg(lambda x: x.sum() / x.count())
goods_by_state = goods_by_state.melt(id_vars="state", value_vars=markets_goods.drop("state", axis=1).columns).rename(columns={"variable": "good", "value": "prop_selling"})
print(goods_by_state)
### To quickly determine if patterns emerge, you choose a subset of goods you find interesting and decide to make a 
### simple text-scatter: the good on the x-axis and the proportion of a state's markets that sell that good on the 
### y-axis.

# Subset goods to interesting ones
to_plot = ['Cheese','Maple','Fruits','Grains','Seafood','Plants','Vegetables']
goods_by_state_small = goods_by_state.query("good in @to_plot")
print(goods_by_state_small)

g = sns.scatterplot(
    data=goods_by_state_small, x="good", y="prop_selling",
    # Hide scatter points by shrinking to nothing
    s=0
)

for _, row in goods_by_state_small.iterrows():
    g.annotate(row["state"], (row["good"], row["prop_selling"]),
               # Center annotation on axis
               ha="center",
               size=10
               )

plt.show()