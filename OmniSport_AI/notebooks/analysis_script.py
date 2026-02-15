import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import os

# Create directory if it doesn't exist
if not os.path.exists("notebooks"):
    os.makedirs("notebooks")

# Set professional theme
sns.set_theme(style="whitegrid")

# --- 1. DATA GENERATION (Simulated Historical Data) ---
print("Generating 100-game dataset for analysis...")
data = []
for i in range(50): 
    data.append({"League": "NBA", "Points": random.randint(95, 135)})
    data.append({"League": "NFL", "Points": random.randint(14, 48)})

df = pd.DataFrame(data)

# --- 2. STATISTICAL SUMMARY ---
print("\n--- Descriptive Statistics ---")
print(df.groupby("League")["Points"].describe())

# --- 3. VISUALIZATION ---
plt.figure(figsize=(10, 6))

sns.boxplot(x="League", y="Points", data=df, palette="magma")

plt.title("OmniSport AI: Scoring Variance Analysis (NBA vs NFL)", fontsize=14)
plt.ylabel("Total Game Points")
plt.xlabel("Sports League")

# Save the chart for the README
plt.savefig("notebooks/scoring_analysis.png")
print("\nSuccess! Chart saved as 'notebooks/scoring_analysis.png'")
plt.show() 