import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Let's use a cleaner, more journalistic style
plt.style.use('fivethirtyeight')

# 1. VISUALIZING GROWTH (Line Plot with Multiple Series)
# Scenario: Comparing our user growth vs. the competitor
months = np.arange(1, 13)
our_growth = [120, 135, 150, 210, 255, 310, 380, 450, 510, 580, 640, 720]
competitor_growth = [200, 210, 220, 230, 250, 270, 290, 310, 340, 380, 410, 440]

plt.figure(figsize=(10, 6))
plt.plot(months, our_growth, label='Our Startup', color='#008fd5', linewidth=3)
plt.plot(months, competitor_growth, label='Legacy Competitor', color='#fc4f30', linestyle='--', linewidth=2)
plt.title("2025 Growth Trajectory: Flipping the Market")
plt.xlabel("Month")
plt.ylabel("Active Users (Thousands)")
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig("01_growth_trajectory.png")
plt.show()

# 2. CUSTOMER SEGMENTS (Rich Scatter Plot)
# Scenario: analyzing customer value vs time spent
np.random.seed(99) # Mixing up the seed
n_users = 60
time_on_site = np.random.uniform(5, 60, n_users) # Minutes
lifetime_value = time_on_site * 3 + np.random.normal(0, 20, n_users)
satisfaction_score = np.random.uniform(1, 10, n_users)

plt.figure(figsize=(10, 6))
# Size of bubble = satisfaction score
plt.scatter(time_on_site, lifetime_value, s=satisfaction_score*30, alpha=0.6, c=satisfaction_score, cmap='coolwarm')
plt.title("Customer Value Matrix")
plt.xlabel("Avg Time on Site (min)")
plt.ylabel("Lifetime Value ($)")
plt.colorbar(label='NPS Score (1-10)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig("02_customer_value_scatter.png")
plt.show()

# 3. REVENUE STREAMS (Grouped Bar Chart)
# Scenario: B2B vs B2C revenue per quarter
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
b2b_rev = [50, 85, 120, 160]
b2c_rev = [80, 75, 70, 65] # Churning a bit on B2C

x_axis = np.arange(len(quarters))
bar_width = 0.35

plt.figure(figsize=(9, 6))
plt.bar(x_axis - bar_width/2, b2b_rev, width=bar_width, label='Enterprise (B2B)', color='#6d904f')
plt.bar(x_axis + bar_width/2, b2c_rev, width=bar_width, label='Consumer (B2C)', color='#e5ae38')
plt.xticks(x_axis, quarters)
plt.title("Revenue Shift: Pivoting to Enterprise")
plt.ylabel("Revenue ($k)")
plt.legend()
plt.savefig("03_revenue_streams.png")
plt.show()

# 4. BURN RATE (Stacked Bar Chart)
# Scenario: Where is the money going?
categories = ['Jan', 'Feb', 'Mar']
salaries = [40, 42, 45]
servers = [10, 12, 15]
marketing = [20, 25, 40] # Big push in March

plt.figure(figsize=(8, 6))
plt.bar(categories, salaries, label='Salaries', color='#30a2da')
plt.bar(categories, servers, bottom=salaries, label='Infrastructure', color='#fc4f30')
# Calculate the bottom for the third stack
bottom_layer_2 = np.array(salaries) + np.array(servers)
plt.bar(categories, marketing, bottom=bottom_layer_2, label='Ad Spend', color='#e5ae38')
plt.title("Q1 Burn Rate Analysis")
plt.legend(loc='upper left')
plt.savefig("04_burn_rate.png")
plt.show()

# 5. LATENCY DISTRIBUTION (Histogram with KDE)
# Scenario: API response times
server_pings = np.random.gamma(2, 2, 1000) # Right-skewed distribution

plt.figure(figsize=(10, 6))
plt.hist(server_pings, bins=30, density=True, alpha=0.7, color='purple', edgecolor='black')
# Adding a manual trend line to look like KDE
x_vals = np.linspace(0, 15, 100)   # <--- GOOD
y_vals = (x_vals * np.exp(-x_vals/2)) / 4 # Approximate Gamma pdf
plt.plot(x_vals, y_vals, color='black', linewidth=2, linestyle='--')
plt.title("API Latency Distribution")
plt.xlabel("Response Time (ms)")
plt.ylabel("Frequency")
plt.savefig("05_latency_histogram.png")
plt.show()

# 6. TEAM PERFORMANCE (Box Plot)
# Scenario: Tickets closed by department
eng_tickets = np.random.normal(50, 10, 50)
supp_tickets = np.random.normal(80, 15, 50)
sales_calls = np.random.normal(40, 20, 50)

plt.figure(figsize=(10, 6))
plt.boxplot([eng_tickets, supp_tickets, sales_calls], labels=['Engineering', 'Support', 'Sales'], patch_artist=True,
            boxprops=dict(facecolor='#ff9999', color='black'),
            medianprops=dict(color='yellow'))
plt.title("Weekly Output Variation by Team")
plt.ylabel("Tasks Completed")
plt.savefig("06_team_performance_box.png")
plt.show()

# 7. UPTIME HEATMAP
# Scenario: Server load across the day
# Generating 7 days x 24 hours of data
load_matrix = np.random.rand(7, 24)
# Make weekends quieter (rows 5 and 6)
load_matrix[5:, :] = load_matrix[5:, :] * 0.5 

plt.figure(figsize=(12, 5))
plt.imshow(load_matrix, aspect='auto', cmap='magma')
plt.colorbar(label='CPU Load %')
plt.title("Server Heatmap: Weekly Load Patterns")
plt.xlabel("Hour of Day")
plt.yticks(np.arange(7), ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
plt.savefig("07_server_heatmap.png")
plt.show()

# 8. EXECUTIVE SUMMARY (Subplot Grid)
# Scenario: The "One-Pager" for investors
fig, ax = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("Q1 Executive Summary", fontsize=20)

# Top Left: Cash Flow
ax[0, 0].plot([1, 2, 3], [100, 90, 85], 'r-o')
ax[0, 0].set_title("Cash Runway (Months)")

# Top Right: New Signups
ax[0, 1].bar(['Jan', 'Feb', 'Mar'], [500, 800, 1200], color='green')
ax[0, 1].set_title("New Signups")

# Bottom Left: Churn
ax[1, 0].pie([95, 5], labels=['Retained', 'Churned'], explode=(0, 0.1), autopct='%1.1f%%')
ax[1, 0].set_title("Retention Rate")

# Bottom Right: NPS
ax[1, 1].hist(np.random.normal(8, 1, 100), bins=10, color='orange')
ax[1, 1].set_title("NPS Distribution")

plt.savefig("08_executive_summary.png")
plt.show()

# 9. THE "MUST SEE" PLOT (Customized)
# Scenario: Highlighting a specific milestone
days = np.arange(30)
users = days ** 2.5

plt.figure(figsize=(10, 6))
plt.plot(days, users, color='#333333')
plt.fill_between(days, users, color='skyblue', alpha=0.3)
plt.title("The 'Hockey Stick' Moment", fontweight='bold')
plt.annotate('Viral Campaign Launch', xy=(20, 20**2.5), xytext=(10, 3000),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.grid(False) # Clean look
plt.savefig("09_viral_growth.png")
plt.show()

# 10. STOCK TRACKER (Time Series)
# Scenario: Tracking our hypothetical stock price
dates = pd.date_range(start="2026-01-01", periods=60)
prices = np.cumsum(np.random.randn(60)) + 50 # Random walk starting at $50

plt.figure(figsize=(12, 6))
plt.plot(dates, prices, linewidth=2)
plt.title("Post-IPO Stock Performance")
plt.gcf().autofmt_xdate() # Fix the dates slanting
plt.savefig("10_stock_series.png")
plt.show()

print("Matplotlib dashboard generated.")