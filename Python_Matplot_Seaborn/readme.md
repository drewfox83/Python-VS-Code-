# 📊 Business Insights & Social Analytics: A Visualization Suite

## Overview
This repository contains a collection of **20 advanced data visualizations** built with Python. 

Rather than generating generic "test plots," I designed this project around two specific, real-world scenarios:
1.  **The Startup Dashboard (Matplotlib):** A business intelligence suite tracking the growth, burn rate, and KPIs of a high-growth tech startup.
2.  **The Remote Work Study (Seaborn):** A statistical analysis exploring the relationship between caffeine, stress, and productivity in a remote work environment.

## 🛠️ Tech Stack
* **Python 3.14+**
* **Matplotlib:** For granular, custom-styled business charts.
* **Seaborn:** For statistical modeling and complex multi-variable relationships.
* **Pandas:** For data manipulation and custom dataset generation.
* **NumPy:** For statistical simulation.

---

## 🚀 Project 1: The Startup Dashboard (Matplotlib)
*Script: `startup_dashboard.py`*

I built this dashboard to simulate the "One-Pager" an analyst would present to investors or a C-Suite team. It uses the `FiveThirtyEight` style sheet for a clean, journalistic look.

**Key Visualizations:**
* **Growth Trajectory:** A multi-series line plot comparing our user acquisition vs. a legacy competitor to highlight market disruption.
* **Burn Rate Analysis:** A stacked bar chart visualizing monthly expenses (Salaries vs. Infrastructure vs. Marketing) to track runway.
* **Server Heatmap:** A 24/7 load analysis to identify peak usage times and infrastructure bottlenecks.
* **The "Hockey Stick" Moment:** A custom-annotated chart highlighting the viral coefficient impact of a specific marketing campaign.

---

## 🧪 Project 2: Remote Work Productivity Study (Seaborn)
*Script: `social_study.py`*

This project simulates a raw dataset of 200 employees to answer the question: *"Does more coffee equals more productivity?"* I used Seaborn to uncover correlations between distinct variables like department, work location, and stress levels.

**Key Insights & Visuals:**
* **The Stress-Productivity Sweet Spot:** A Joint Plot (Hexbin) revealing that while moderate stress correlates with focus, high stress correlates with diminishing returns.
* **Departmental Deep Dives:** Boxen and Violin plots splitting productivity metrics by "Manager" vs. "Individual Contributor" roles.
* **Caffeine Consumption:** A stacked distribution analysis showing which departments rely most heavily on coffee (spoiler: it's Sales).
* **Correlation Matrix:** A heatmap identifying statistically significant relationships between time spent working and output quality.

---

## 💻 How to Run This Project

### 1. Prerequisites
You will need Python installed along with the data science stack. You can install all dependencies with:

```bash
pip install matplotlib seaborn pandas numpy