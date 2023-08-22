import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

pollution = pd.read_csv("../datasets/pollution_wide.csv")
## Comparing with 2 KDEs
# Filter dataset to the year 2012
sns.kdeplot(
    data=pollution[pollution.year == 2012],
    x="O3",
    # Shade under kde and add a helpful label
    ## shade=True,
    fill=True,
    label="2012"
)

# Filter dataset to everything except the year 2012

sns.kdeplot(
    # Filter dataset to the year 2012
    data=pollution[pollution.year != 2012],
    x="O3",
    # Shade under kde and add a helpful label
    ## shade=True,
    fill=True,
    label="other years"
)
plt.legend()
plt.show()

## Improving your KDEs

# sns.distplot(
#     pollution[pollution.city == "Vandenberg Air Force Base"].O3,
#     label="Vandenberg",
#     hist=False,
#     color="steelblue",
#     rug=True
# )
sns.kdeplot(
    data=pollution[pollution.city == "Vandenberg Air Force Base"],
    x="O3",
    label="Vandenberg",
    color="steelblue"
)
sns.rugplot(
    data=pollution[pollution.city == "Vandenberg Air Force Base"],
    x="O3"
)

# sns.distplot(
#     pollution[pollution.city != "Vandenberg Air Force Base"].O3,
#     label="Other cities",
#     hist=False,
#     color="gray",
# )

sns.kdeplot(
    data=pollution[pollution.city != "Vandenberg Air Force Base"],
    x="O3",
    label="Other cities",
    color="gray"
)

plt.legend()
plt.show()

## Beeswarms
# Filter data to just March
pollution_march = pollution[pollution.month == 3]
sns.swarmplot(
    data=pollution_march,
    x="O3",
    y="city",
    hue="city",
    # Decrease the size of the points to avoid crowding
    size=3
)

plt.title("March Ozone levels by city")
plt.show()