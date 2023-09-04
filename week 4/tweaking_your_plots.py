import matplotlib.pyplot as plt
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

markets_goods = markets.drop(["FMID", "name", "city", "county", "lat", "lon", "months_open", "state_pop"], axis=1)
goods_by_state = markets_goods.groupby("state", as_index=False).agg(lambda x: x.sum() / x.count())
goods_by_state = goods_by_state.melt(id_vars="state", value_vars=markets_goods.drop("state", axis=1).columns).rename(columns={"variable": "good", "value": "prop_selling"})
# print(goods_by_state)
goods_by_state = goods_by_state.query("good in ['Cheese', 'Eggs', 'Fruits', 'Maple', 'Poultry', 'Wine']")
print(goods_by_state)

## Cleaning up the background
### While exploring state-level patterns in goods sold at farmer's markets, a few states stood out to you. North 
### Dakota and New Mexico routinely fell near the bottom of the states regarding their proportion of farmer's markets 
### selling a given good. Whereas Vermont was always near the top. You want to present the general patterns in good 
### sales by state, while also highlighting the states you found interesting.
### You make a scatter plot of goods being sold by the proportion of markets that sell that good in a state. To 
### highlight the interesting states, you draw a line between each of the state's points. To make a clean and minimal 
### plot, you reduce the background to a simple set of orienting grids.

# Set background to white with grid
sns.set_style("whitegrid")

plt.scatter(data=goods_by_state, x="good", y="prop_selling", marker="_", alpha=0.7)

# Draw lines across goods for highlighted states
highlighted = goods_by_state.query("state in ['New Mexico','North Dakota','Vermont']")
sns.lineplot(data=highlighted, x="good", y="prop_selling", hue="state", legend=False)

# Draw state name at end of lines
last_rows = highlighted.groupby("state", as_index = False).agg("first")
for _,row in last_rows.iterrows():
    plt.annotate(
        row["state"], (row["good"], row["prop_selling"]),
        ha="right", xytext=(5,0), textcoords="offset pixels"
    )

# Remove all borders
sns.despine(left=True, bottom=True)
plt.show()

## Remixing a plot
### You find the relationship between the latitude of a farmer's market and the number of months the market was open 
### fascinating. Intuitively as one gets further South, the growing seasons are longer, and thus the markets can stay 
### open longer. To visualize this story, you summarize the market data at the state level and draw a heatmap with 
### columns corresponding to the duration the markets are open. Each row in the heatmap shows the distribution of the 
### market "season" for a state and rows are sorted in descending order of the state's latitude.
## image[latheatmap.png]

### The default heatmap leaves a lot to be desired. Decrease the font size to allow each state name to fit without 
### overlap. The dark color palette also clashes with the light background, and the colorbar doesn't help the reader 
### as the point is relative comparisons.
markets_by_month = markets[["state", "months_open", "name"]].groupby(["state", "months_open"]).count()
print(markets_by_month)

markets_by_month.name = markets_by_month.name.div(markets.state.value_counts())
markets_by_month.reset_index(inplace=True)

markets_by_month = markets_by_month.pivot_table(index="state", columns="months_open", values="name", fill_value=0)

state_by_lat = pd.Index(['North Dakota', 'Washington', 'Montana', 'Minnesota', 'Oregon', 'Idaho', 'Maine', 'South Dakota', 'Vermont', 'Wisconsin', 'Michigan', 'New Hampshire', 'Wyoming', 'Massachusetts', 'New York',
       'Iowa', 'Rhode Island', 'Connecticut', 'Nebraska', 'Illinois', 'Ohio', 'New Jersey', 'Pennsylvania', 'Indiana', 'Utah', 'Colorado', 'Delaware', 'Maryland', 'West Virginia',
       'District of Columbia', 'Kansas', 'Nevada', 'Missouri', 'Virginia', 'Kentucky', 'California', 'Tennessee', 'Oklahoma', 'North Carolina', 'Arkansas', 'New Mexico', 'South Carolina', 'Georgia',
       'Arizona', 'Alabama', 'Mississippi', 'Texas', 'Louisiana', 'Florida'], name="← Latitude")
# Decrease font size so state names are less crowded
sns.set(font_scale=0.85)

# Switch to an appropriate color palette
blue_pal = sns.light_palette("steelblue", as_cmap=True)

# Order states by latitude
g = sns.heatmap(
    data=markets_by_month.reindex(state_by_lat),
    # Add gaps between cells
    linewidths=0.1,
    # Set new palette and remove color bar 
    cmap=blue_pal, cbar=False,
    yticklabels=True
)
g.set_yticklabels(g.get_yticklabels(), rotation = 0)
plt.title('Distribution of months open for farmers markets by latitude')
plt.show()

## Enhancing legibility
### You and your colleagues have decided that the most important aspect of the data you want to show is the 
### differences between the most "market-friendly" state, Vermont, and the least, Texas. To do this, put two plots 
### side by side – a barplot showing the number of people per farmer's market in the state and a scatter plot showing 
### the population on the x-axis and the number of markets on the y-axis.
### Emphasize your findings by calling out Vermont and Texas by assigning them distinct colors. Also, provide a large 
### and easy to read annotation for Texas.
### Supplied is a vector state_colors that assigns Vermont and Texas unique colors and all other states gray along 
### with the annotation describing Texas, tx_message.
markets = pd.read_csv("../datasets/markets_cleaned.csv")
state_population = pd.read_csv("../datasets/census-state-populations.csv")
state_population.columns = ["state", "state_pop"]
markets = pd.merge(markets, state_population, on="state", how="inner")

markets_by_state = markets.groupby("state", as_index=False).agg(
    num_markets=pd.NamedAgg(column="name", aggfunc="size"),
    population=pd.NamedAgg(column="state_pop", aggfunc=lambda x: x.iloc[0]),
)
markets_by_state["people_per_market"] = markets_by_state["population"] / markets_by_state["num_markets"]
markets_by_state.sort_values(by="people_per_market", inplace=True)
print(markets_by_state)
state_colors = ['steelblue'] + ['gray'] * (markets_by_state.shape[0] - 2) + ["orangered"]
print(state_colors)
tx_message = "Texas has a large population\nand relatively few farmers\nmarkets."

_, (ax1, ax2) = plt.subplots(1, 2)
# Draw barplot w/ colors mapped to state_colors vector
sns.barplot(data=markets_by_state, x="people_per_market", y="state", palette=state_colors, ax=ax1)

# Map state colors vector to the scatterplot as well
p = sns.scatterplot(data=markets_by_state, x="population", y="num_markets", c=state_colors, s=60, ax=ax2)

# Log the x and y scales of our scatter plot so it's easier to read
ax2.set(xscale="log", yscale="log")

# Increase annotation text size for legibility
ax2.annotate(tx_message, xy = (26956958,230), 
             xytext = (26956958, 450),ha = 'right', 
             size = 15, backgroundcolor = 'white',
             arrowprops = {'facecolor':'black', 'width': 3})

sns.set_style('whitegrid')
plt.show()