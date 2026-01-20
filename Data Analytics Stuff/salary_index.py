import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt

# --- Real Markert Data (Rough Jan. 2026 EStimates) ---
city_market_data = [
    {
        'City': 'New York, NY', 
        'Nominal_Salary': 50000, # Top of my projected range 
        'Rent_Yearly': 24000, # ~ 2,000/mo (Studio in Queens/Roomates) 
        'Tax_Rate': 0.20,  # ~ 20% (Lower bracket + City/State tax)
        'Groceries_Index': 1.35 # Cost of good is still high 
    },
    {
        'City': 'San Francisco, CA', 
        'Nominal_Salary': 50000, # Top of Range 
        'Rent_Yearly': 24000, # ~2,000/mo (Roomates needed)
        'Tax_Rate': 0.20,  # ~20% (Lower bracket + State tax) 
        'Groceries_Index': 1.45 # Cost of good is still high 
    },
    {
        'City': 'Jackson, MS', 
        'Nominal_Salary': 40000,    # Top of your range 
        'Rent_Yearly': 9600,  #~ $800/mo (Decent 1NR apartment)
        'Tax_Rate': 0.14, #~14% (Lower Tax burden)
        'Groceries_Index': 0.94 # Cheaper goods 
    }, 
    {
        'City': 'Tampa, FL', 
        'Nominal_Salary': 42000,  # Mid-range
        'Rent_Yearly': 14400, # ~1,200/mo
        'Tax_Rate': 0.12,  # ~ 12% (No State Income tax )
        'Groceries_Index': 1.02
    },
    {
        'City': 'Austin, TX', 
        'Nominal_Salary': 45000, # Mid-ranged
        'Rent_Yearly': 15600, # ~1,300/mo (Studio)
        'Tax_Rate': 0.12,  # ~12% (No State Income Tax)
        'Groceries_Index': 0.96
    }
]

df = pd.DataFrame(city_market_data) 

# --- 2. Financial Modeling ---

# Step A: Remove Taxes (Net Pay) 
df['Net_Pay'] = df['Nominal_Salary'] * (1 - df['Tax_Rate'])

# Step B: Remove Housing (Discretionary Income) 
df['Discretionary_Income'] = df['Net_Pay'] - df['Rent_Yearly']

# Step C: Normalize for Cost of Goods (The "Real Wage") 
df['Real_Purchasing_Power'] = df['Discretionary_Income'] / df['Groceries_Index']


# --- 3. Visualization --- 
# Reshape for plotting 
df_melted = df.melt(
    id_vars="City", 
    value_vars=["Nominal_Salary", "Real_Purchasing_Power"], 
    var_name="Metric", 
    value_name="Dollars"
)

# Rename for Legend Readability 
df_melted['Metric'] = df_melted['Metric'].replace({
    'Nominal_Salary': 'Gross Salary (on Paper)', 
    'Real_Purchasing_Power': 'Real Purchasing Power (Adjusted)' 
})

plt.figure(figsize=(12, 7))
sns.set_theme(style="white") 

# Color Palette: Grey for "Gross", Green for "Real Wealth" 
custom_palette = ["#95a5a6", "#27ae60"]

bar_plot = sns.barplot(
    data=df_melted, 
    x="Dollars", 
    y="City", 
    hue="Metric", 
    palette=custom_palette, 
    orient='h'
)


# Add Reference Line for Jackson (Your Baseline) 
# We use a try/except block jut in case the data is missing, to prevent crashes

try: 
    jackson_val = df[df['City']=='Jackson, MS']['Real_Purchasing_Power'].values[0]
    plt.axvline(x=jackson_val, color='green', linestyle='--', linewidth=2, label=f'Jackson Baseline (${jackson_val:,.0f})')
except IndexError: 
               pass

# Formatting 
plt.title("Entry-Level Analysis ($40k-$50k): Real Purchasing Power", fontsize=14, weight='bold') 
plt.xlabel("Annual Value ($)", fontsize=12) 
plt.ylabel("") 
plt.legend(loc='lower right') 

sns.despine(left=True, bottom=True) 
plt.tight_layout()

print("Entry-Level Analysis Complete.") 
plt.show()