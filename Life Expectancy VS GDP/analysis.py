import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------------------------------------
# 1. SETUP & DATA LOADING
# -----------------------------------------------------------
# Set the visual style for all plots (makes them look professional)
sns.set_theme(style='whitegrid', context='notebook')

# Check if file exists to prevent crashing if the path is wrong
file_name = 'all_data.csv'
if not os.path.exists(file_name):
    print(f"❌ ERROR: The file '{file_name}' was not found.")
    print("   Make sure the CSV file is in the same folder as this script.")
    exit()

# Load the dataset directly from the file
df = pd.read_csv(file_name)
print("✅ Data loaded successfully.")

# -----------------------------------------------------------
# 2. VERIFICATION (Proof it reads YOUR file)
# -----------------------------------------------------------
# This prints the countries found inside the CSV to the terminal
unique_countries = df['Country'].unique()
print(f"\nI found {len(df)} rows of data.")
print(f"The countries in this file are: {unique_countries}")

# -----------------------------------------------------------
# 3. PRE-PROCESSING
# -----------------------------------------------------------
# Rename the long column for easier coding
# 'Life expectancy at birth (years)' -> 'Life_Exp'
df.rename(columns={'Life expectancy at birth (years)': 'Life_Exp'}, inplace=True)

# -----------------------------------------------------------
# 4. SUMMARY STATISTICS (The Averages)
# -----------------------------------------------------------
# Calculate the average Life Expectancy and GDP for each country
df_means = df.drop("Year", axis=1).groupby("Country").mean().reset_index()

print("\n--- Average Values per Country ---")
print(df_means)

# -----------------------------------------------------------
# 5. VISUALIZATION: GLOBAL AVERAGES
# -----------------------------------------------------------
# Plot 1: Average Life Expectancy
plt.figure(figsize=(10, 6))
sns.barplot(x="Life_Exp", y="Country", data=df_means, palette="viridis", hue="Country")
plt.title("Average Life Expectancy by Country")
plt.xlabel("Life Expectancy (Years)")
plt.show()

# Plot 2: Average GDP
plt.figure(figsize=(10, 6))
sns.barplot(x="GDP", y="Country", data=df_means, palette="viridis", hue="Country")
plt.title("Average GDP by Country (USD)")
plt.xlabel("GDP (Trillions of Dollars)")
plt.show()

# -----------------------------------------------------------
# 6. VISUALIZATION: DISTRIBUTIONS (Violin Plots)
# -----------------------------------------------------------
# 
# Violin plots show the "shape" of the data.
# A long shape (like Zimbabwe) means high volatility/change over time.
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

sns.violinplot(ax=axes[0], x="Life_Exp", y="Country", data=df, palette="magma", hue="Country")
axes[0].set_title("Distribution of Life Expectancy")

sns.violinplot(ax=axes[1], x="GDP", y="Country", data=df, palette="magma", hue="Country")
axes[1].set_title("Distribution of GDP")

plt.tight_layout()
plt.show()

# -----------------------------------------------------------
# 7. VISUALIZATION: TRENDS OVER TIME (Line Charts)
# -----------------------------------------------------------
# We use FacetGrid to create a separate chart for EVERY country automatically.
# 'sharey=False' is crucial so small economies don't look like flat lines.

# Trend 1: GDP Growth
g_gdp = sns.FacetGrid(df, col="Country", col_wrap=3, height=4, sharey=False, hue="Country")
g_gdp.map(sns.lineplot, "Year", "GDP")
g_gdp.add_legend()
g_gdp.fig.suptitle("GDP Growth Over Time (2000-2015)", y=1.02, fontsize=14)
plt.show()

# Trend 2: Life Expectancy
g_life = sns.FacetGrid(df, col="Country", col_wrap=3, height=4, sharey=False, hue="Country")
g_life.map(sns.lineplot, "Year", "Life_Exp")
g_life.add_legend()
g_life.fig.suptitle("Life Expectancy Trends (2000-2015)", y=1.02, fontsize=14)
plt.show()

# -----------------------------------------------------------
# 8. VISUALIZATION: CORRELATION (Scatter Plots)
# -----------------------------------------------------------
# Shows the relationship between Wealth (GDP) and Health (Life Exp)
g_corr = sns.FacetGrid(df, col="Country", col_wrap=3, height=4, sharey=False, sharex=False, hue="Country")
g_corr.map(sns.scatterplot, "Life_Exp", "GDP")
g_corr.add_legend()
g_corr.fig.suptitle("Correlation: Life Expectancy vs. GDP", y=1.02, fontsize=14)
plt.show()