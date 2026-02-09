import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. Loading and Inspecting the Data
# ==========================================
# Let's start by loading the datasets to see what we're working with.
species = pd.read_csv('species_info.csv')
observations = pd.read_csv('observations.csv')

print(f"Species shape: {species.shape}")
print(f"Observations shape: {observations.shape}")

# Take a peek at the first few rows
print("\n--- Species Preview ---")
print(species.head())

print("\n--- Observations Preview ---")
print(observations.head())

# ==========================================
# 2. Data Cleaning & Preparation
# ==========================================
# Upon inspection, the 'conservation_status' column has many NaN values.
# In this dataset, a NaN value implies the species is not under any specific 
# conservation status (i.e., they are stable).
# Let's replace these NaNs with "No Intervention" to make the data clearer.

species.fillna(value={"conservation_status": "No Intervention"}, inplace=True)

# Let's verify the different conservation categories we have now.
print("\n--- Conservation Categories ---")
print(species.conservation_status.unique())

# ==========================================
# 3. Analysis: Conservation Status by Category
# ==========================================
# A great first question to ask is: "Which group of animals is most at risk?"
# Let's filter out the "No Intervention" species to focus on the ones in trouble.

conservation_concern = species[species.conservation_status != "No Intervention"]

# Now, let's visualize the breakdown of protected species by category (Mammal, Bird, etc.)
plt.figure(figsize=(12, 8))
ax = sns.countplot(x="conservation_status", hue="category", data=conservation_concern)
plt.title("Conservation Status by Species Category")
plt.xlabel("Conservation Status")
plt.ylabel("Number of Species")
plt.legend(title="Category")
plt.show()
plt.clf() # Clear the plot for the next one

# ==========================================
# 4. Deep Dive: Are Mammals more protected?
# ==========================================
# The previous chart was a bit crowded. Let's create a new column 'is_protected'
# to simply see which categories have the highest percentage of protected species.

species['is_protected'] = species.conservation_status != 'No Intervention'

# Group by category to see the percentages
category_counts = species.groupby(['category', 'is_protected']).scientific_name.nunique().reset_index()
category_pivot = category_counts.pivot(columns='is_protected', index='category', values='scientific_name').reset_index()
category_pivot.columns = ['category', 'not_protected', 'protected']

# Calculate the percentage of protected species
category_pivot['percent_protected'] = category_pivot.protected / (category_pivot.protected + category_pivot.not_protected)

print("\n--- Percentage of Protected Species by Category ---")
print(category_pivot.sort_values(by='percent_protected', ascending=False))

# ==========================================
# 5. Species Spotlight: The Gray Wolf
# ==========================================
# Analysts often need to answer specific questions about one animal.
# Let's look at the "Gray Wolf" and see where it is spotted most often.

species['is_wolf'] = species.common_names.apply(lambda x: "Wolf" in x)
wolves = species[species.is_wolf]

# Merge the wolf data with the observations table to get the counts per park
wolf_observations = wolves.merge(observations)

print("\n--- Wolf Observations ---")
print(wolf_observations.head())

# Let's visualize the total wolf sightings per park
plt.figure(figsize=(12, 6))
sns.barplot(x="park_name", y="observations", data=wolf_observations, estimator=sum, ci=None)
plt.title("Observations of Wolves across National Parks")
plt.xlabel("National Park")
plt.ylabel("Number of Observations")
plt.xticks(rotation=30) # Rotate labels so they don't overlap
plt.show()
plt.clf()