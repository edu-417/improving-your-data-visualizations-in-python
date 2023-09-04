import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

## Looking at the farmers market data
### Loaded is a new dataset, markets. Each row of this DataFrame belongs to an individual farmers market in the 
### continental United States with various information about the market contained in the columns. In this exercise, 
### explore the columns of the data to get familiar with them for future analysis and plotting.
### As a first step, print out the first three lines of markets to get an idea of what type of data the columns encode. 
### Then look at the summary descriptions of all of the columns. Since there are so many columns in the DataFrame, 
### you'll want to turn the results 'sideways' by transposing the output to avoid cutting off rows.
markets = pd.read_csv("../datasets/markets_cleaned.csv")
state_population = pd.read_csv("../datasets/census-state-populations.csv")
state_population.columns = ["state", "state_pop"]
markets.dropna(subset=["months_open"], inplace=True)
markets.drop_duplicates(inplace=True)
markets = markets[~markets.isin(["Alaska", "Hawaii"])]
markets["num_items_sold"] = markets.drop(["FMID", "name", "city", "county", "state", "lat", "lon", "months_open"], axis=1).sum(axis=1)
markets = pd.merge(markets, state_population, on="state", how="inner")
# Print first three rows of data and transpose
first_rows = markets.head(3).transpose()
print(first_rows)

# Get descriptions of every column
col_descriptions = markets.describe(percentiles=[0.5], include="all").transpose()
print(col_descriptions)

## Scatter matrix of numeric columns
### You've investigated the new farmer's market data, and it's rather wide – with lots of columns of information for 
### each market's row. Rather than painstakingly going through every combination of numeric columns and making a 
### scatter plot to look at correlations, you decide to make a scatter matrix using the pandas built-in function.
### Increasing the figure size with the figsize argument will help give the dense visualization some breathing room. 
### Since there will be a lot of overlap for the points, decreasing the point opacity will help show the density of 
### these overlaps.

# Select just the numeric columns (exluding individual goods)
numeric_columns = ['lat', 'lon', 'months_open', 'num_items_sold', 'state_pop']

# Make a scatter matrix of numeric columns
pd.plotting.scatter_matrix(
    markets[numeric_columns],
    # Make figure large to show details
    figsize=(15, 10),
    # Lower point opacity to show overlap
    alpha=0.5
)

plt.show()

## Digging in with basic transforms
### You are curious to see if the population of a state correlates to the number of items sold at farmer's markets. 
### To check this, take the log of the population and draw a scatter plot against the number of items sold by a market. 
### From your previous explorations of the dataset, you know there will be a lot of overlap, so to get a better handle 
### on the patterns you want to reduce the marker opacity.

# Create a new logged population column 
markets["log_pop"] = np.log(markets["state_pop"])

# Draw a scatterplot of log-population to # of items sold
sns.scatterplot(
    data=markets, x="log_pop", y="num_items_sold",
    # Reduce point opacity to show overlap
    alpha=0.25
)
plt.show()