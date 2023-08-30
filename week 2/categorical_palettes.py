import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

pollution = pd.read_csv("../datasets/pollution_wide.csv")

## Using a custom categorical palette

pollution_jan13 = pollution.query("year == 2013 & month == 1")

sns.lineplot(data=pollution_jan13, x="day", y="CO", palette="Set2", hue="city", linewidth=3)
plt.show()

## Dealing with too many categories

## Coloring ordinal categories
pollution_2013 = pollution.query("year == 2013").copy()
city_pollution_2013 = pollution_2013[["city", "month", "CO", "NO2", "O3", "SO2"]].groupby(["city", "month"]).agg("mean")
city_pollution_2013["CO"] = (city_pollution_2013["CO"] - pollution_2013["CO"].mean()) / pollution_2013["CO"].std()
city_pollution_2013["O3"] = (city_pollution_2013["O3"] - pollution_2013["O3"].mean()) / pollution_2013["O3"].std()
city_pollution_2013["NO2"] = (city_pollution_2013["NO2"] - pollution_2013["NO2"].mean()) / pollution_2013["NO2"].std()
city_pollution_2013["SO2"] = (city_pollution_2013["SO2"] - pollution_2013["SO2"].mean()) / pollution_2013["SO2"].std()
# city_pollution_2013.columns = ["city", "month", "gas", "value"]
city_pollution_2013 = city_pollution_2013.stack().reset_index()
city_pollution_2013.columns = ["city", "month", "pollutant", "value"]
city_pollution_2013["city_pol"] = city_pollution_2013["city"] + " " + city_pollution_2013["pollutant"]
city_pol_month = city_pollution_2013[["city_pol", "month", "value"]].sort_values(["city_pol", "month"]).copy()
# print(city_pol_month.sort_values(["city_pol", "month"]))
# Choose the combos that get distinct colors
wanted_combos = ['Vandenberg Air Force Base NO2', 'Long Beach CO', 'Cincinnati SO2']

# Assign a new column to DataFrame for isolating the desired combos
city_pol_month['color_cats'] = [x if x in wanted_combos else 'other' for x in city_pol_month['city_pol']]

# Plot lines with color driven by new column and lines driven by original categories
sns.lineplot(
    data=city_pol_month,
    x="month",
    y="value",
    hue = 'color_cats',
    units = 'city_pol',
    estimator = None,
    palette = 'Set2',
    linewidth=3
)
plt.show()

## Coloring ordinal categories

# Divide CO into quartiles
pollution["CO quartile"] = pd.qcut(pollution["CO"], q=4, labels=False)
# Filter to just Des Moines
des_moines = pollution.query("city == 'Des Moines'")

# Color points with by quartile and use ColorBrewer palette
sns.scatterplot(data=des_moines, x="SO2", y="NO2", hue="CO quartile", palette="GnBu")
plt.show()

## Choosing the right variable to encode with color

max_pollutant_values = pollution[["city", "year", "CO", "NO2", "O3", "SO2"]].groupby(["city", "year"]).agg("max")
max_pollutant_values = max_pollutant_values.stack().reset_index()
max_pollutant_values.columns = ["city", "year", "pollutant", "value"]

cities = ['Fairbanks', 'Long Beach', 'Vandenberg Air Force Base', 'Denver', 
          'Indianapolis', 'Des Moines', 'Cincinnati', 'Houston']

city_maxes = max_pollutant_values[max_pollutant_values.city.isin(cities)]

sns.catplot(x = 'year', hue = 'city',
              y = 'value', row = 'pollutant',    
              data = city_maxes, palette = 'muted',
              sharey = False, kind = 'bar')
plt.show()


# Reduce to just cities in the western half of US
cities = ['Fairbanks', 'Long Beach', 'Vandenberg Air Force Base', 'Denver']
# Filter data to desired cities
city_maxes = max_pollutant_values[max_pollutant_values.city.isin(cities)]

# Swap city and year encodings
sns.catplot(x = 'city', hue = 'year',
              y = 'value', row = 'pollutant',    
              # Change palette to one appropriate for ordinal categories
              data = city_maxes, palette = 'BuGn',
              sharey = False, kind = 'bar')
plt.show()