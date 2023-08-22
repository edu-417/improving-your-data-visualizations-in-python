import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

pollution = pd.read_csv("../datasets/pollution_wide.csv")

#Hardcoding a highlight
houston_pollution = pollution[pollution.city == "Houston"]

# Make array orangred for day 330 of year 2014, otherwise lightgray
houston_colors = [
    "orangered"
    if (day == 330) & (year == 2014)
    else "lightgray"
    for day, year in zip(houston_pollution.day, houston_pollution.year)
]

sns.regplot(
    data=houston_pollution,
    x="NO2",
    y="SO2",
    fit_reg=False,
    # Send scatterplot argument to color points
    scatter_kws={"facecolors": houston_colors, "alpha": 0.7}
)
# plt.show()

#Programmatically creating a highlight

houston_pollution = pollution[pollution.city == "Houston"].copy()
# Find the highest observed O3 value
max_O3 = houston_pollution.O3.max()

# Make a column that denotes which day had highest O3
houston_pollution["point_type"] = [
    "Highest O3 Day"
    if O3 == max_O3
    else "Others"
    for O3 in houston_pollution.O3
]

sns.scatterplot(data=houston_pollution, x="NO2", y="SO2", hue="point_type")
plt.show()