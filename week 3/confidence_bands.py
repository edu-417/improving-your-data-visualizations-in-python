import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

pollution = pd.read_csv("../datasets/pollution_wide.csv")
## Making a confidence band
### Vandenberg Air Force Base is often used as a location to launch rockets into space.
### You have a theory that a recent increase in the pace of rocket launches could be harming the air quality in the 
### surrounding region. To explore this, you plotted a 25-day rolling average line of the measurements of 
### atmospheric NO2. To help decide if any pattern observed is random-noise or not, you decide to add a 
### 99% confidence band around your rolling mean. Adding a confidence band to a trend line can help shed light on 
### the stability of the trend seen. This can either increase or decrease the confidence in the discovered trend.
pollution_vandenberg = pollution.query("city == 'Vandenberg Air Force Base' and year == 2012")
vandenberg_NO2 = pollution_vandenberg[["city", "year", "month", "day", "NO2"]].copy()
vandenberg_NO2_rolling = vandenberg_NO2["NO2"].rolling(25)
vandenberg_NO2["mean"] = vandenberg_NO2_rolling.agg("mean")
vandenberg_NO2["std_err"] = vandenberg_NO2_rolling.agg(lambda x: x.sem(ddof=0))
vandenberg_NO2.dropna(inplace=True)
vandenberg_NO2.reset_index(inplace=True)
# vandenberg_NO2.columns = ["day", "mean", "std_err"]
print(vandenberg_NO2)

# Draw 99% inverval bands for average NO2
vandenberg_NO2["lower"] = vandenberg_NO2["mean"] - 2.58 * vandenberg_NO2["std_err"]
vandenberg_NO2["upper"] = vandenberg_NO2["mean"] + 2.58 * vandenberg_NO2["std_err"]

# Plot mean estimate as a white semi-transparent line
plt.plot("day", "mean", data=vandenberg_NO2, color="white", alpha=0.4)

# Fill between the upper and lower confidence band values
plt.fill_between(x="day", y1="lower", y2="upper", data=vandenberg_NO2, alpha=0.4)
plt.show()

## Separating a lot of bands
### It is relatively simple to plot a bunch of trend lines on top of each other for rapid and precise comparisons.
### Unfortunately, if you need to add uncertainty bands around those lines, the plot becomes very difficult to read.
### Figuring out whether a line corresponds to the top of one class' band or the bottom of another's can be hard due
### to band overlap. Luckily in Seaborn, it's not difficult to break up the overlapping bands into separate faceted plots.
### To see this, explore trends in SO2 levels for a few cities in the eastern half of the US. If you plot the trends 
### and their confidence bands on a single plot - it's a mess. To fix, use Seaborn's FacetGrid() function to spread 
### out the confidence intervals to multiple panes to ease your inspection.
eastern_cities = ['Cincinnati', 'Des Moines', 'Houston', 'Indianapolis']
eastern_pollution = pollution.query("city in @eastern_cities and year == 2014")
eastern_SO2 = eastern_pollution[["city", "year", "month", "day", "SO2"]].copy()
eastern_SO2["mean"] = eastern_SO2["SO2"].rolling(20).agg("mean")
eastern_SO2["std_err"] = eastern_SO2["SO2"].rolling(20).agg(lambda x: x.sem(ddof=0))
eastern_SO2.dropna(inplace=True)
eastern_SO2.reset_index(inplace=True)

eastern_SO2["lower"] = eastern_SO2["mean"] - 1.96 * eastern_SO2["std_err"]
eastern_SO2["upper"] = eastern_SO2["mean"] + 1.96 * eastern_SO2["std_err"]
print(eastern_SO2)


# Setup a grid of plots with columns divided by location
g = sns.FacetGrid(data=eastern_SO2, col="city", col_wrap=2)

# Map interval plots to each cities data with coral colored ribbons
g.map(plt.fill_between, "day", "lower", "upper", color="coral")

# Map overlaid mean plots with white line
g.map(plt.plot, "day", "mean", color="white")
plt.show()

## Cleaning up bands for overlaps
### You are working for the city of Denver, Colorado and want to run an ad campaign about how much cleaner Denver's air 
### is than Long Beach, California's air. To investigate this claim, you will compare the SO2 levels of both cities for
### the year 2014 (provided as the DataFrame SO2_compare). Since you are solely interested in how the cities compare, 
### you want to keep the bands on the same plot. To make the bands easier to compare, decrease the opacity of the 
### confidence bands and set a clear legend.
pollution_compare = pollution.query("year == 2014 and city in ['Denver', 'Long Beach']")
SO2_compare = pollution_compare[["city", "year", "month", "day", "SO2"]].copy()
SO2_compare["mean"] = SO2_compare["SO2"].rolling(20).agg("mean")
SO2_compare["std_err"] = SO2_compare["SO2"].rolling(20).agg(lambda x: x.sem(ddof=0))
SO2_compare.dropna(inplace=True)
SO2_compare.reset_index(inplace=True)

SO2_compare["lower"] = SO2_compare["mean"] - 1.96 * SO2_compare["std_err"]
SO2_compare["upper"] = SO2_compare["mean"] + 1.96 * SO2_compare["std_err"]
print(SO2_compare)

for city, color in [('Denver',"#66c2a5"), ('Long Beach', "#fc8d62")]:
    # Filter data to desired city
    city_data = SO2_compare[SO2_compare.city == city]

    # Set city interval color to desired and lower opacity
    plt.fill_between(data=city_data, x="day", y1="lower", y2="upper", color=color, alpha=0.4)

    # Draw a faint mean line for reference and give a label for legend
    plt.plot("day", "mean", data=city_data, label=city, color=color, alpha=0.25)

plt.legend()
plt.show()