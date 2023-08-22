import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

pollution = pd.read_csv("../datasets/pollution_wide.csv")

# A basic text annotation
sns.scatterplot(
    data=pollution[pollution.month==8],
    x="CO",
    y="SO2"
)

plt.text(
    x=0.57,
    y=41,
    s="Cincinnati had highest observed\nSO2 value on Aug 11, 2013",
    fontdict={
        "ha": "left",
        "size": "large"
    }
)

plt.show()

## Arrow annotations
# Query and filter to New Years in Long Beach
january_pollution = pollution.query("(month == 1) & (year == 2012)")
longbeach_newyears = january_pollution.query("(day == 1) & (city == 'Long Beach')")

sns.scatterplot(data=january_pollution, x="CO", y="NO2")

# Point arrow to lb_newyears & place text in lower left 
plt.annotate(
    "Long Beach New Years",
    xy=(longbeach_newyears.CO, longbeach_newyears.NO2),
    xytext=(2., 15.),
    arrowprops={
        "facecolor": "gray",
        "width": 3,
        "shrink": 0.03
    },
    backgroundcolor="white",
)

plt.show()

# Combining annotations and color

is_longbeach = ["orangered" if city == "Long Beach" else "lightgray" for city in pollution.city]
sns.regplot(
    data=pollution,
    x="CO",
    y="O3",
    fit_reg=False,
    scatter_kws={
        "facecolors": is_longbeach,
        "alpha": 0.3
    }
)

plt.text(x=1.6, y=0.072, s="April 30th, Bad Day")
plt.show()