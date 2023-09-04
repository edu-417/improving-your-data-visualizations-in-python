import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

pollution = pd.read_csv("../datasets/pollution_wide.csv")
## The bootstrap histogram
### You are considering a vacation to Cincinnati in May, but you have a severe sensitivity to NO2. You pull a few years 
### of pollution data from Cincinnati in May and look at a bootstrap estimate of the average NO2 levels. You only have 
### one estimate to look a
# t the best way to visualize the results of your bootstrap estimates is with a histogram.
### While you like the intuition of the bootstrap histogram by itself, your partner who will be going on the vacation 
### with you, likes seeing percent intervals. To accommodate them, you decide to highlight the 95% interval by shading 
### the region.

cinci_may_NO2 = pollution.query("city  ==  'Cincinnati' & month  ==  5").NO2
def bootstrap(data, n_boots):
    return [ np.mean( np.random.choice(data, len(data)) ) for _ in range(n_boots) ]
# Generate bootstrap samples
boot_means = bootstrap(cinci_may_NO2, 1000)

# Get lower and upper 95% interval bounds
lower, upper = np.percentile(boot_means, [2.5, 97.5])

# Plot shaded area for interval
plt.axvspan(lower, upper, color="gray", alpha=0.2)

# Draw histogram of bootstrap samples
#sns.distplot(boot_means, bins=100, kde=False) ##deprecated
sns.histplot(data=boot_means, bins=100, alpha=0.6)
plt.show()

## Bootstrapped regressions
### While working for the Long Beach parks and recreation department investigating the relationship between NO2 and SO2 
### you noticed a cluster of potential outliers that you suspect might be throwing off the correlations.
pollution_may = pollution.query("month == 5")
long_beach_may_pollution = pollution_may.query("city == 'Long Beach'")
no2_so2 = long_beach_may_pollution[["year", "month", "day", "NO2", "SO2"]].copy()
no2_so2_boot = pd.concat([
    no2_so2.sample(len(no2_so2), replace=True).assign(sample=i)
    for i in range(70)
])
print(no2_so2)
print(no2_so2_boot)

sns.lmplot(
    data=no2_so2_boot, x="NO2", y="SO2",
    # Tell seaborn to a regression line for each sample
    hue="sample",
    # Make lines blue and transparent
    line_kws={"color": "steelblue", "alpha": 0.2},
    # Disable built-in confidence intervals
    ci=None, legend=False, scatter=False
)

# Draw scatter of all points
plt.scatter('NO2', 'SO2', data=no2_so2)
plt.show()

## Lots of bootstraps with beeswarms
### As a current resident of Cincinnati, you're curious to see how the average NO2 values compare to Des Moines, 
### Indianapolis, and Houston: a few other cities you've lived in.
### To look at this, you decide to use bootstrap estimation to look at the mean NO2 values for each city. Because the 
### comparisons are of primary interest, you will use a swarm plot to compare the estimates.
### The DataFrame pollution_may is provided along with the bootstrap() function seen in the slides for performing your 
### bootstrap resampling.

# Initialize a holder DataFrame for bootstrap results
city_boots = pd.DataFrame()

for city in ["Cincinnati", "Des Moines", "Indianapolis", "Houston"]:
    # Filter to city
    city_NO2 = pollution_may[pollution_may.city == city].NO2
    # Bootstrap city data & put in DataFrame
    cur_boot = pd.DataFrame({"NO2_avg": bootstrap(city_NO2, 100), 'city': city})
    # Append to other city's bootstraps
    city_boots = pd.concat([city_boots, cur_boot])

print(city_boots)
# Beeswarm plot of averages with citys on y axis
sns.swarmplot(data=city_boots, y="city", x="NO2_avg", color="coral", size=4)
plt.show()