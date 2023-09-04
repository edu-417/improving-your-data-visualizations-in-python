import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

markets = pd.read_csv("../datasets/markets_cleaned.csv")
markets.dropna(subset=["months_open"], inplace=True)
markets.drop_duplicates(inplace=True)
markets = markets[~markets.state.isin(["Alaska", "Hawaii", "Puerto Rico"])]
print(markets.describe(include="all").transpose())

state_population = pd.read_csv("../datasets/census-state-populations.csv")
state_population.columns = ["state", "state_pop"]
markets = pd.merge(markets, state_population, on="state", how="inner")

## Stacking to find trends
### In the farmers market dataset, you are interested in the number of months that a market stays open in relation to 
### its geography, more specifically its longitude. You're curious to see if there are any regions of the country that 
### behave noticeably different from the others.
### To do this, you create a basic map with a scatter plot of the latitude and longitude of each market, coloring each 
### market by the number of months it's open. Further digging into the latitude relationship, you draw a regression 
### plot of the latitude to the number of months open with a flexible fit line to determine if any trends appear. You 
### want to view these simultaneously to get the clearest picture of the trends.

# Setup two stacked plots
_, (ax1, ax2) = plt.subplots(2, 1)

# Draw location scatter plot on first plot
sns.scatterplot(
    data=markets, x="lon", y="lat", hue="months_open",
    palette=sns.light_palette("orangered", n_colors=12),
    legend=False,
    ax=ax1
)

# Plot a regression plot on second plot
sns.regplot(
    data=markets, x="lon", y="months_open",
    scatter_kws={"alpha": 0.2, "color": "gray"},
    lowess=True,
    marker="|",
    ax=ax2
)
plt.show()

## Using a plot as a legend
### One interesting thread of investigation in the farmer's market data is a state's "market friendliness" and 
### specifically, the outliers. One way to look at this is by using the ratio of farmer's markets to people by state. 
### You could directly look at the ratio; however, a ratio throws away the raw information about a state's population 
### and the number of markets. A large state with a high ratio could be more interesting than a small one.
### You can show both the ratio and raw numbers by drawing two plots, one of the ratio and the other of the market 
### number to population scatter plot. To help simplify your now dense visualization, you can use the bar plot as a 
### legend; calling out interesting states by matching the colors of their bars and scatter points.

markets_by_state = markets.groupby("state", as_index=False).agg(
    num_markets=pd.NamedAgg(column="name", aggfunc="size"),
    population=pd.NamedAgg(column="state_pop", aggfunc=lambda x: x.iloc[0]),
)
markets_by_state["people_per_market"] = markets_by_state["population"] / markets_by_state["num_markets"]
markets_by_state["log_pop"] = np.log(markets_by_state["population"])
markets_by_state["log_markets"] = np.log(markets_by_state["num_markets"])
markets_by_state["is_selected"] = markets_by_state["state"].apply(lambda state: state if state in ["Maryland", "Texas", "Vermont"] else "other")

markets_by_state.sort_values(by="people_per_market", inplace=True)

print(markets_by_state)

# Set up two side-by-side plots
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 15))

# Map the column for selected states to the bar color
sns.barplot(
    data=markets_by_state, x="people_per_market", y="state", hue="is_selected",
    palette="tab10",
    # Disable dodge so bars are full size
    dodge=False,
    ax=ax1
)

# Map selected states to point color
sns.scatterplot(
    data=markets_by_state, x="log_pop", y="log_markets", hue="is_selected",
    palette="tab10",
    ax=ax2,
    s=250
)
ax1.legend_.remove()
ax2.legend_.remove()
plt.show()