import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

pollution = pd.read_csv("../datasets/pollution_wide.csv")

## Getting rid of unnecessary color
# Hard to read scatter of CO and NO2 w/ color mapped to city
# sns.scatterplot('CO', 'NO2',
#                 alpha = 0.2,
#                 hue = 'city',
#                 data = pollution)

# Setup a facet grid to separate the cities apart
# g = sns.FacetGrid(data=pollution, hue="city", col="city", col_wrap=3)
g = sns.FacetGrid(data=pollution, col="city", col_wrap=3)
g.map(sns.scatterplot, "CO", "NO2", alpha=0.2)
plt.show()

## Fixing Seaborn's bar charts
import numpy as np

# sns.barplot(data=pollution, x="CO", y="city", estimator=np.mean, ci=False, edgecolor="black")
sns.barplot(data=pollution, x="CO", y="city", estimator=np.mean, errorbar=("ci", False), edgecolor="black")
plt.show()

sns.barplot(data=pollution, x="CO", y="city", estimator=np.mean, errorbar=("ci", False), color="cadetblue")
plt.show()