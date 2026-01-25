import seaborn as sns
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 

# --- Configuration ---
# "Talk" context makes the fonts slightly larger and easier to read in a portfolio 
sns.set_theme(style="whitegrid", context="talk") 

# --- Generating Custom Data ---
# Scenario: A study on "Remote Work Productivity" with 200 participants 
# We can create a dataframe from scractch so the data tells a specific story. 
np.random.seed(2026)
n = 200

data = {
    'Hours_Worked': np.random.normal(8, 1.5, n), 
    'Coffee_Cups': np.random.randint(0, 6, n), 
    'Productivity_Score': np.random.uniform(50, 100, n),
    'Department': np.random.choice(['Tech', 'HR', 'Sales', 'Creative'], n),
    'Location': np.random.choice(['Home', 'Office', 'Cafe'], n), 
    'Stress_Level': np.random.choice(['Low', 'Med', 'High'], n)
}

# Add some "human" correlation: More coffee = slightly more stress
data['Stress_Score'] = data['Coffee_Cups'] * 10 + np.random.normal(0, 5, n) 

df = pd.DataFrame(data) 
print("Data generated successfully. Starting Visualization...") 
# --- 1. Regression Plot ---
# Question: Do longer hours actually lead to higher score? 
plt.figure(figsize=(10, 6))
sns.regplot(data=df, x='Hours_Worked', y='Productivity_Score',
            scatter_kws={'alpha':0.5, 'color': '#2b7bba'}, line_kws={'color': '#e84d5b'})

plt.title("Efficiency Paradox: Hours vs. Output")
plt.tight_layout()
plt.savefig("sns_01_regression.png")
plt.close() # Frees up memory
print("saved 01_regression.png") 

# --- 2. Distribution With Hue --- 
# Question: Which department runs on the most caffeine? 
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Coffee_Cups', hue='Department', multiple='stack', palette='viridis') 
plt.title("Caffeine Consumption by Dept") 
plt.tight_layout()
plt.savefig("sns_02_dist_hue.png") 
plt.close()
print("Saved 02_dist_hue.png") 

# --- 3. Joint Plot (Hexbin) --- 
# Question: Where is the 'Sweet Spot' between stress and productivity?
# Note: JointGrid creates its own figure, so we don't use plt.figure()
g = sns.jointplot(data=df, x='Stress_Score', y='Productivity_Score', kind='hex', color='#4CB391')
g.fig.suptitle("The Stress-Productivity Sweet Spot", y=1.02) 
plt.savefig("sns_03_joint_plot.png") 
plt.close() 
print("Saved 03_joint_plot.png") 

# --- 4. Count Plot --- 
# Question: Where do people choose to work? 
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='Location', hue='Stress_Level', palette='pastel') 
plt.title("Work Location Preferences & Stress") 
plt.tight_layout() 
plt.savefig("sns_04_count_plot.png") 
plt.close()
print("Saved 04_count_plot.png") 

# --- 5. Box Plot By Category ---
# Question: Which environment yields the best results?
plt.figure(figsize=(10, 6))
# Using standard palette to avoid warnings
sns.boxplot(data=df, x='Location', y='Productivity_Score', palette='Set2') 
# Adding raw points (stripplot) on top shows we aren't hiding data 
sns.stripplot(data=df, x='Location', y='Productivity_Score', color='black', alpha=0.3)
plt.title("Where Do We Get the Most Done?") 
plt.tight_layout()
plt.savefig("sns_05_box_cat.png") 
plt.close()
print("Saved 05_box_cat.png") 

# --- 6. Violing Plot Split --- 
# Question: Do Managers work more or less hours that ICs? 
# Create a fake binary variable for this plot 
df['Role'] = np.random.choice(['Manager', 'IC'], n) 

plt.figure(figsize=(10, 6))
sns.violinplot(data=df, x='Department', y='Hours_Worked', hue='Role', 
               split=True, inner='quartile', palette='muted')
plt.title("Hours Worked: Managers vs. Individual Contributors") 
plt.tight_layout()
plt.savefig("sns_06_violin_split.png") 
plt.close() 
print("Saved 06_violin_split.png") 

# --- 7. Correlation Heatmap --- 
# Question: What variables actually matter? 
# Select only numeric columns for to avoid crashes 
numeric_cols = df.select_dtypes(include=[np.number]) 
corr = numeric_cols.corr() 

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='RdBu_r', center=0) 
plt.title("Variable Correlation Matrix") 
plt.tight_layout() 
plt.savefig("sns_07_heatmap.png") 
plt.close() 
print("Saved 07_heatmap.png") 

# --- 8. Pair Plot --- 
# Overview of relationships 
# We subset the data to keep the chart clean 
pair_df = df[['Hours_Worked', 'Productivity_Score', 'Stress_Score', 'Location']]
sns.pairplot(pair_df, hue='Location', markers=["o", "s", "D"])
plt.savefig("sns_08_pair_pot.png") 
plt.close()
print("Saved 08_pair_plot.png") 

# --- 9. Facet Grid --- 
# Breaking down productivity by Stress Level 
g = sns.FacetGrid(df, col="Stress_Level", height=5) 
g.map(sns.scatterplot, "Hours_Worked", "Productivity_Score", alpha=0.6) 
g.add_legend() 
plt.savefig("sns_08_facet_grid.png") 
plt.close()
print("Saved 09_facet_grid.png") 

# --- 10. Complex Panel (Boxen Plot) --- 
# A more detailed look at distribution tails (useful for outliers) 
plt.figure(figsize=(12, 6))
sns.boxenplot(data=df, x='Department', y='Productivity_Score', palette='rocket') 
plt.title("Deep Dive: Productivity Tails by Department") 
plt.tight_layout() 
plt.savefig("sns_10_complex_panel.png") 
plt.close() 
print("Saved 10_complex_panel.png") 

print("-----------------------------------------------")
print("Social Study Visualization Complete!")
print("Check your folder for 10 new 'sns_' images.") 
print("-----------------------------------------------") 