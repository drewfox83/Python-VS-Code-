import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pybaseball import batting_stats

# --- Configuration ---
SEASON = 2025
MIN_PA = 200 # Only looking at platers with > 200 Plate Apperances

# --- 1. Getting Real Perfomance Data ---
print(f"Fetching MLB {SEASON} batting stats... (This scrapes Baseball-Reference)")
# 'qual' ensures we don't get pitchers or bench players with skewed stats 
df_stats = batting_stats(SEASON, qual=MIN_PA) 

# Keep only what we need to keep it clean 
df_stats = df_stats[['Name', 'Team', 'HR', 'WAR', 'OPS']]


# --- 2. THE FINANCIAL MERGE --- 
# In a corporate setting, this would be a SQL join
# Since salary APIs are private, we manually map widely public 2025 salaries. 
real_salaries_2025 = {
    'Shohei Ohtani': 70.0, 
    'Aaron Judge': 40.0, 
    'Mike Trout': 37.1, 
    'Anthony Rendon': 38.0, 
    'Corey Seager': 35.0, 
    'Francisco Lindor': 34.1, 
    'Carlos Correa': 33.3, 
    'Gincarlo Stanton': 32.0, 
    'Bryce Harper': 27.5, 
    'Freddie Freeman': 27.0, 
    'Mookie Betts': 30.0, 
    'Trea Turner': 27.2, 
    'Juan Soto': 31.0, # Est. Arbitration/Contract
    'Matt Olson': 22.0, 
    'Ronald Acuna Jr.': 17.0, 
    'Rafael Devers': 29.0, 
    'Austin Riley': 21.0,
    'Fernando Tatis Jr.': 24.0, 
    'Vladimir Guerrero Jr.': 19.9,
    'Pete Alonso': 20.5
}

# Map the dictionary to a new column
# Line 47 (Corrected):
df_stats['Salary_Millions'] = df_stats['Name'].map(real_salaries_2025)

# Filter: We can only analyze players where we have BOTH stats and salary
df_analysis = df_stats.dropna(subset=['Salary_Millions']).copy()


# --- 3. The Analyst Logic (ROI) ---
# Metric: Cost per Home Run ($ Millions paid per HR) 
df_analysis['Cost_Per_HR'] = df_analysis['Salary_Millions'] / df_analysis['HR']


# --- 3. Visualization ---
plt.figure(figsize=(12, 8))
sns.set_theme(style="whitegrid") 

# Create Bubble Chart
scatter = sns.scatterplot(
    data=df_analysis, 
    x='HR', 
    y='Salary_Millions', 
    size='Cost_Per_HR',  # Bubble sixe = Inefficiency
    sizes=(50, 800),  # Range of bubble sizes
    hue='Cost_Per_HR',   # Color = Inefficiency
    palette='viridis',   # Reverse palette: Purple/Blue (Low Cost) is Good
    alpha=0.7, 
    edgecolor='black'
)

# Label every player 
for i in range(len(df_analysis)): 
    row = df_analysis.iloc[i]
    plt.text(
        row['HR'] + 0.5,
        row['Salary_Millions'],
        row['Name'], 
        weight='semibold', 
        size=9
    )

# Formatting 
plt.title(f"MLB {SEASON}: ROI Analysis of Top Earners", fontsize=16, weight='bold') 
plt.xlabel(f"Home Runs ({SEASON}) Actual)", fontsize=12) 
plt.ylabel("2025 Salary ($ Millions)", fontsize=12) 
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', title="Cost per HR ($M)")
plt.tight_layout()

print("Analysis Complete. Plotting...") 
plt.show()