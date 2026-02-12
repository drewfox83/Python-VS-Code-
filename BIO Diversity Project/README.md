# 🌲 Biodiversity in National Parks

## Project Overview
This project serves as a mock data analysis for the **National Parks Service**. The goal is to analyze biodiversity data to identify patterns in the conservation status of different species and understand how observation frequency varies across four major national parks.

By investigating this data, I aimed to answer questions such as:
* **Which categories of species are most at risk?** (e.g., Are mammals more endangered than birds?)
* **What is the distribution of conservation status for these species?**
* **Where are specific animals, such as the Gray Wolf, most frequently observed?**

## 📂 Data Sources
The project utilizes two CSV files provided by Codecademy:
1.  **`species_info.csv`**: Contains data about different species, including their scientific names, common names, category (Mammal, Bird, etc.), and conservation status.
2.  **`observations.csv`**: Records the number of times a specific species was observed in a specific park.

## 🛠️ Tools & Libraries Used
* **Python**: The core programming language for the analysis.
* **Pandas**: Used for data manipulation, cleaning (handling `NaN` values), and aggregation.
* **Matplotlib & Seaborn**: Used to create visualizations (bar charts, count plots) to communicate findings effectively.

## 🔍 Key Steps & Methodology

### 1. Data Inspection & Cleaning
* Loaded the datasets and inspected the structure (columns, data types, missing values).
* **Handling Missing Data**: The `conservation_status` column contained significant missing values (`NaN`). Through analysis, I determined that these values represented species with "No Intervention" (i.e., structurally stable populations). I imputed these values to ensure accurate visualization.

### 2. Exploratory Data Analysis (EDA)
* I calculated the distribution of species across conservation categories (`Species of Concern`, `Endangered`, `Threatened`, `In Recovery`).
* I created a **Pivot Table** to calculate the percentage of protected species within each category (Mammal, Bird, Amphibian, etc.).

### 3. Data Visualization
* **Conservation Status**: Visualized the count of species in each conservation category, broken down by species type.
* **Wolf Observations**: Filtered the data to isolate "Gray Wolf" sightings and plotted their observation counts across the four national parks (Yellowstone, Yosemite, Great Smoky Mountains, Bryce).

## 📊 Key Findings

* **Conservation Disparities**: Certain categories, such as **Mammals** and **Birds**, showed a higher percentage of protected status compared to others like Reptiles.
* **The "Species of Concern" Category**: This was by far the largest category for protected species, indicating that while many species are being monitored, fewer are critically endangered.
* **Wolf Populations**: The analysis of Gray Wolf data revealed distinct differences in observation frequency, with **Yellowstone National Park** showing significantly higher sighting numbers compared to others.

## 🚀 How to Run
1.  Clone this repository.
2.  Ensure `species_info.csv` and `observations.csv` are in the same directory as the script.
3.  Run the notebook or Python script:
    ```bash
    python biodiversity.py
    ```

---
*This project was completed as part of the Codecademy Data Science Career Path.*