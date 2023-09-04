import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

pollution = pd.read_csv("../datasets/pollution_wide.csv")
## 90, 95, and 99% intervals
### You are a data scientist for an outdoor adventure company in Fairbanks, Alaska. Recently, customers have been 
### having issues with SO2 pollution, leading to costly cancellations. The company has sensors for CO, NO2, and O3 but 
### not SO2 levels.
### You've built a model that predicts SO2 values based on the values of pollutants with sensors (loaded as 
### pollution_model, a statsmodels object). You want to investigate which pollutant's value has the largest effect on 
### your model's SO2 prediction. This will help you know which pollutant's values to pay most attention to when 
### planning outdoor tours. To maximize the amount of information in your report, show multiple levels of uncertainty 
### for the model estimates.
fairbanks_pollution = pollution.query("city == 'Fairbanks'").reset_index()
y = fairbanks_pollution.SO2
X = fairbanks_pollution[["day", "CO", "NO2", "O3"]]
X = X.apply(lambda col: (col - col.min()) / (col.max() - col.min()))
X = sm.add_constant(X)
pollution_model = sm.OLS(y, X).fit()
print(pollution_model.summary())

# Add interval percent widths
alphas = [     0.01,  0.05,   0.1] 
widths = [ '99% CI', '95%', '90%']
colors = ['#fee08b','#fc8d59','#d53e4f']

for alpha, color, width in zip(alphas, colors, widths):
    # Grab confidence interval
    conf_ints = pollution_model.conf_int(alpha)

    # Pass current interval color and legend label to plot
    plt.hlines(y=conf_ints.index, xmin=conf_ints[0], xmax=conf_ints[1], colors=color, label=width, linewidth=10)

# Draw point estimates
plt.plot(pollution_model.params, pollution_model.params.index, "wo", label="Point Estimate")
plt.legend()
plt.show()

## 90 and 95% bands
### You are looking at a 40-day rolling average of the NO2 pollution levels for the city of Cincinnati in 2013. To 
### provide as detailed a picture of the uncertainty in the trend you want to look at both the 90 and 99% intervals 
### around this rolling estimate.
### To do this, set up your two interval sizes and an orange ordinal color palette. Additionally, to enable precise 
### readings of the bands, make them semi-transparent, so the Seaborn background grids show through.
cincinnati_pollution_2013 = pollution.query("city == 'Cincinnati' and year == 2013")
cinci_13_no2 = cincinnati_pollution_2013[["year", "month", "day", "NO2"]].copy()
cinci_13_no2["mean"] = cincinnati_pollution_2013["NO2"].rolling(40).agg("mean")
cinci_13_no2["std_err"] = cincinnati_pollution_2013["NO2"].rolling(40).agg(lambda x: x.sem(ddof=0))
cinci_13_no2.dropna(inplace=True)
cinci_13_no2.reset_index(inplace=True)
print(cinci_13_no2)

int_widths = ['90%', '99%']
z_scores = [1.67, 2.58]
colors = ['#fc8d59', '#fee08b']

for percent, Z, color in zip(int_widths, z_scores, colors):
    # Pass lower and upper confidence bounds and lower opacity
    plt.fill_between(x=cinci_13_no2.day, y1=cinci_13_no2["mean"] - Z * cinci_13_no2["std_err"], y2=cinci_13_no2["mean"] + Z * cinci_13_no2["std_err"], color = color, alpha=0.4, label=percent)

plt.legend()
plt.show()

##Using band thickness instead of coloring
### You are a researcher investigating the elevation a rocket reaches before visual is lost and pollutant levels at 
### Vandenberg Air Force Base. You've built a model to predict this relationship (stored in the DataFrame 
### rocket_height_model), and since you are working independently, you don't have the money to pay for color figures 
### in your journal article. You need to make your model results plot work in black and white. To do this, you will 
### plot the 90, 95, and 99% intervals of the effect of each pollutant as successively smaller bars.
rocket_model = pd.read_csv("../datasets/rocket_model.csv")

# Decrase interval thickness as interval widens
sizes =      [    15,  10,  5]
int_widths = ['90% CI', '95%', '99%']
z_scores =   [    1.67,  1.96,  2.58]

for percent, Z, size in zip(int_widths, z_scores, sizes):
    plt.hlines(y = rocket_model.pollutant, 
               xmin = rocket_model['est'] - Z*rocket_model['std_err'],
               xmax = rocket_model['est'] + Z*rocket_model['std_err'],
               label = percent, 
               # Resize lines and color them gray
               linewidth = size, 
               color = 'gray') 
    
# Add point estimate
plt.plot('est', 'pollutant', 'wo', data = rocket_model, label = 'Point Estimate')
plt.legend(loc = 'center left', bbox_to_anchor = (1, 0.5))
plt.show()