import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# average_ests = pd.read_csv("../datasets/pollution_average_stats.csv")
pollution = pd.read_csv("../datasets/pollution_wide.csv")
## Basic confidence intervals
### You are a data scientist for a fireworks manufacturer in Des Moines, Iowa. You need to make a case to the city 
### that your company's large fireworks show has not caused any harm to the city's air. To do this, you look at the 
### average levels for pollutants in the week after the fourth of July and how they compare to readings taken after 
### your last show. By showing confidence intervals around the averages, you can make a case that the recent 
### readings were well within the normal range.
### This data is loaded as average_ests with a row for each measured pollutant.
pollution_desmoines = pollution.query("city == 'Des Moines' and NO2 >= 19 and month == 7")
# pollution_desmoines = pollution_desmoines.query("day >= 186 + (year == 2012) and day < 193 + (year == 2012)")
print(pollution_desmoines)
average_stats = pollution_desmoines.pivot_table(values=["CO", "NO2", "O3", "SO2"], columns="city", aggfunc=["mean", lambda x: x.sem(ddof=0)]).reset_index()
average_stats.columns = ["pollutant", "mean", "std_err"]
average_stats["y"] = "95% Interval"
average_stats["seen"] = [0.4, 16.0, 0.05, 0.15 ]
print(average_stats)

# # Construct CI bounds for averages
# average_ests["lower"] = average_ests["mean"] - 1.96 * average_ests["std_err"]
# average_ests["upper"] = average_ests["mean"] + 1.96 * average_ests["std_err"]

# # Setup a grid of plots, with non-shared x axes limits
# g = sns.FacetGrid(data=average_ests, row="pollutant", sharex=False)

# # Plot CI for average estimate
# g.map(plt.hlines, "y", "lower", "upper")

# # Plot observed values for comparison and remove axes labels
# g.map(plt.scatter, "seen", "y", color="orangered").set_ylabels("").set_xlabels("")
# plt.show()

average_stats["lower"] = average_stats["mean"] - 1.96 * average_stats["std_err"]
average_stats["upper"] = average_stats["mean"] + 1.96 * average_stats["std_err"]

# Setup a grid of plots, with non-shared x axes limits
g = sns.FacetGrid(data=average_stats, row="pollutant", sharex=False)

# Plot CI for average estimate
g.map(plt.hlines, "y", "lower", "upper")

# Plot observed values for comparison and remove axes labels
g.map(plt.scatter, "seen", "y", color="orangered").set_ylabels("").set_xlabels("")
plt.show()

##Annotating confidence intervals
### Your data science work with pollution data is legendary, and you are now weighing job offers in both Cincinnati, 
### Ohio and Indianapolis, Indiana. You want to see if the SO2 levels are significantly different in the two cities, 
### and more specifically, which city has lower levels. To test this, you decide to look at the differences in the 
### cities' SO2 values (Indianapolis' - Cincinnati's) over multiple years (provided as diffs_by_year).
### Instead of just displaying a p-value for a significant difference between the cities, you decide to look at the 
### 95% confidence intervals (columns lower and upper) of the differences. This allows you to see the magnitude of 
### the differences along with any trends over the years.
pollution_city = pollution.query("city == 'Cincinnati' or city == 'Indianapolis'")
pollution_SO2 = pollution_city[["year", "month", "day", "city", "SO2"]].groupby(["year", "month", "day", "city"]).mean().unstack().dropna().reset_index()
pollution_SO2.columns = ["year", "month", "day", "Cincinnati", "Indianapolis"]
pollution_SO2["diff"] = pollution_SO2["Cincinnati"] - pollution_SO2["Indianapolis"]

diffs_by_year = pollution_SO2[["year", "diff"]].groupby(["year"]).agg(["mean", lambda x: x.sem(ddof=0)]).reset_index()
diffs_by_year.columns = ["year", "mean", "std_err"]
diffs_by_year["lower"] = diffs_by_year["mean"] - 1.96 * diffs_by_year["std_err"]
diffs_by_year["upper"] = diffs_by_year["mean"] + 1.96 * diffs_by_year["std_err"]

# Set start and ends according to intervals 
# Make intervals thicker
plt.hlines(data=diffs_by_year, y="year", xmin="lower", xmax="upper", linewidth=5, color="steelblue", alpha=0.7)

# Point estimates
plt.plot('mean', 'year', 'k|', data=diffs_by_year)

# Add a 'null' reference line at 0 and color orangered
plt.axvline(x=0, color="orangered", linestyle="--")

# Set descriptive axis labels and title
plt.xlabel('95% CI')
plt.title('Avg SO2 differences between Cincinnati and Indianapolis')
plt.show()