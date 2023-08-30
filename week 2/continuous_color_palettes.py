import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

pollution = pd.read_csv("../datasets/pollution_wide.csv")

## Making a custom continuous palette
cincinnati_2014 = pollution.query("city == 'Cincinnati' & year == 2014")

# Define a custom continuous color palette
color_palette = sns.light_palette("orangered", as_cmap=True)

sns.scatterplot(data=cincinnati_2014, x="CO", y="NO2", hue="O3", palette=color_palette)
plt.show()

## Customizing a diverging palette heatmap
nov_2015_pollution = pollution.query("month == 11 & year == 2015").copy()
nov_2015_pollution["day"] -= 305
nov_2015_pollution["norm_CO"] = (nov_2015_pollution["CO"] - nov_2015_pollution["CO"].mean()) / nov_2015_pollution["CO"].std()
nov_2015_CO = nov_2015_pollution.pivot(index="city", columns="day", values="norm_CO")

# Define a custom palette
color_palette = sns.diverging_palette(250, 0, as_cmap=True)

sns.heatmap(data=nov_2015_CO, vmin=-4, vmax=4, cmap=color_palette, center=0)
plt.show()

## Adjusting your palette according to context

oct_2015_pollution = pollution.query("month == 10 & year == 2015").copy()
oct_2015_pollution["day"] -= 274
oct_2015_pollution["norm_O3"] = (oct_2015_pollution["O3"] - oct_2015_pollution["O3"].mean()) / oct_2015_pollution["O3"].std()
oct_2015_O3 = oct_2015_pollution.pivot(index="city", columns="day", values="norm_O3")
print(oct_2015_O3)

# Dark plot background
# plt.style.use("dark_background")

# Modify palette for dark background
color_palette = sns.diverging_palette(
    250, 0, center = 'dark', as_cmap = True
)

sns.heatmap(oct_2015_O3, cmap=color_palette, center=0)
plt.show()
