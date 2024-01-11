import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


"""
First, let's have an overview of the revenue of the portfolio each year. For that, I will create a chart that will be populated with other mini-charts, representing
each one of them all the years of the transactions. In each one of those plots, it could be seen the evolution of the revenue on a given year.
"""
monthlydata = pd.read_csv("monthlyData.csv")

# Adapt the data to make it easier to visualize it
monthlydata['Month Revenue'] = monthlydata['Month Revenue']/1000

# Plot each year's time series in its own facet
sns.set_theme(style="dark")

g = sns.relplot(
    data=monthlydata,
    x="Month", y="Month Revenue", col="Year", hue="Year",
    kind="line", palette="crest", linewidth=4, zorder=5,
    col_wrap=3, height=2, aspect=1.5, legend=False,
)

# Iterate over each subplot to customize further
for year, ax in g.axes_dict.items():

    # Add the title as an annotation within the plot
    ax.text(.8, .85, year, transform=ax.transAxes, fontweight="bold")

    # Plot every year's time series in the background
    sns.lineplot(
        data=monthlydata, x="Month", y="Month Revenue", units="Year",
        estimator=None, color=".7", linewidth=1, ax=ax,
    )

# Reduce the frequency of the x axis ticks
ax.set_xticks(ax.get_xticks()[::3])

# Tweak the supporting aspects of the plot
g.set_titles("Monthly Revenue per Year")
g.set_axis_labels("Months", "Revenue per Month")
g.tight_layout()

# Save the plot in the same folder as the script
plt.savefig('Charts\month_revenue_evolution.png')

#Show the chart
plt.show()

"""
HEATMAP

Let's create now a heatmap to see which is the best period of the year for the portfolio. This will gave a more direct way to see which are the best and worst period(s) of the portfolio
"""

# Load the example flights dataset and convert to long-form
monthRevenues = (
    monthlydata
    .pivot(index="Month", columns="Year", values="Month Performance")
)

# Draw a heatmap with the numeric values in each cell
f, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(monthRevenues, annot=True, linewidths=.5, ax=ax)

# Save the plot in the same folder as the script
plt.savefig('Charts\month_revenue_heatmap.png')

#Show the chart
plt.show()

"""
Now let's create a chart for the yearly data. Let see the behaviour of the Year Revenue, Year Performance and Total Amount through the years.
"""

sns.set_theme(style="whitegrid")

# Read the .csv file
yearlyData = pd.read_csv("yearlyData.csv")

# Manipulate the data to visualize it correctly. To do that, I will only select the year revenue and total amount to be plotted.
dates = yearlyData['Year']
selected_columns = ['Year Revenue', 'Total Amount']
values = yearlyData[selected_columns].values
data = pd.DataFrame(values, dates, columns=["Year Revenue", "Total Amount"])

sns.lineplot(data=data, palette="tab10", linewidth=2.5)

# Save the plot in the same folder as the script
plt.savefig('Charts\yearly_revenue_amount.png')

#Show the chart
plt.show()