"""
Project: T.H.A.N.O.S. Housing Protocol
Description: Proprietary valuation and heuristic optimization system for Real Estate data.
Author: T.H.A.N.O.S. Inc.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

# Configuration for professional output
pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:,.2f}'.format
sns.set_theme(style="whitegrid")

def run_housing_protocol():
    print(">>> Initializing T.H.A.N.O.S. Housing Protocol...\n")
    
    # ==========================================
    # PHASE 1: [T] TAKE INGESTION
    # ==========================================
    print("[T] Taking Ingestion (Loading Data)...")
    
    # Using the standard Ames Housing dataset (or Kaggle House Prices train.csv)
    # We will try to load from a standard remote source if local file is missing.
    file_path = 'train.csv'
    url = 'https://raw.githubusercontent.com/ryanleeallred/datasets/master/Ames%20Housing%20Data/train.csv'
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        print("    Status: Local 'train.csv' loaded.")
    else:
        print(f"    Status: Local file missing. Fetching Ames Housing data from remote...")
        df = pd.read_csv(url)
        
    print(f"    Dimensions: {df.shape[0]} rows, {df.shape[1]} columns")
    print("-" * 40)

    # ==========================================
    # PHASE 2: [H] HEAL DATA (Quick Check)
    # ==========================================
    # (Not explicitly required by PDF, but necessary for calculations)
    print("[H] Healing Critical Nulls...")
    
    # Fill missing values for columns we need to calculate features
    cols_to_fix = ['LotFrontage', 'MasVnrArea', 'GarageYrBlt']
    for col in cols_to_fix:
        if col in df.columns:
            df[col] = df[col].fillna(0)
            
    print("    Status: Critical numeric nulls filled with 0.")
    print("-" * 40)

    # ==========================================
    # PHASE 3: [A] AUGMENT FEATURES
    # ==========================================
    # PDF Requirements: TotalSF, HouseAge, WasRemodeled, TotalBath, HasGarage/Pool/Fireplace, PricePerSqFt
    print("[A] Augmenting Features (Engineering)...")
    
    # 1. TotalSF (Total Square Footage)
    # Combining 1st Floor, 2nd Floor, and Basement
    df['TotalSF'] = df['1stFlrSF'] + df['2ndFlrSF'] + df['TotalBsmtSF']
    
    # 2. HouseAge (Current Year - YearBuilt)
    # Assuming 'YrSold' is the reference point
    df['HouseAge'] = df['YrSold'] - df['YearBuilt']
    
    # 3. WasRemodeled (Binary: 1 if Remodel Year != Build Year)
    df['WasRemodeled'] = (df['YearRemodAdd'] != df['YearBuilt']).astype(int)
    
    # 4. TotalBath (Full + 0.5 * Half)
    # Summing all bathrooms above grade and in basement
    df['TotalBath'] = (df['FullBath'] + (0.5 * df['HalfBath']) + 
                       df['BsmtFullBath'] + (0.5 * df['BsmtHalfBath']))
    
    # 5. Binary Flags (HasGarage, HasPool, HasFireplace)
    df['HasGarage'] = df['GarageArea'].apply(lambda x: 1 if x > 0 else 0)
    df['HasPool'] = df['PoolArea'].apply(lambda x: 1 if x > 0 else 0)
    df['HasFireplace'] = df['Fireplaces'].apply(lambda x: 1 if x > 0 else 0)
    
    # 6. PricePerSqFt (Value Metric)
    df['PricePerSqFt'] = df['SalePrice'] / df['TotalSF']
    
    print("    Generated: TotalSF, HouseAge, WasRemodeled, TotalBath, PricePerSqFt")
    print("    Generated: HasGarage, HasPool, HasFireplace")
    print("-" * 40)

    # ==========================================
    # PHASE 4: [N] NARROW INSIGHTS (Correlation)
    # ==========================================
    # PDF Requirement: Correlation Analysis
    print("[N] Narrowing Insights (Correlation)...")
    
    # Select numeric features of interest
    features = ['SalePrice', 'TotalSF', 'OverallQual', 'HouseAge', 'TotalBath', 'PricePerSqFt']
    corr_matrix = df[features].corr()
    
    # Display Correlation Matrix
    print("\n    [Correlation Matrix with SalePrice]")
    print(corr_matrix[['SalePrice']].sort_values(by='SalePrice', ascending=False))
    
    # Plotting Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('T.H.A.N.O.S. Correlation Analysis')
    print("    Status: Heatmap generated (Check popup).")
    plt.show()
    print("-" * 40)

    # ==========================================
    # PHASE 5: [O] OBSERVE STATISTICS
    # ==========================================
    # PDF Requirement: Neighborhood analysis, Price by categorical features
    print("[O] Observing Statistics...")
    
    # 1. Neighborhood Analysis (Top 5 Most Expensive)
    print("\n    [Top 5 Neighborhoods by Average Price]")
    neighborhood_stats = df.groupby('Neighborhood')['SalePrice'].mean().sort_values(ascending=False)
    print(neighborhood_stats.head(5))
    
    # 2. Price by Quality (Categorical)
    print("\n    [Price by Overall Quality (1-10)]")
    quality_stats = df.groupby('OverallQual')['SalePrice'].median()
    print(quality_stats.tail(5)) # Show top qualities
    
    print("-" * 40)

    # ==========================================
    # PHASE 6: [S] SERIALIZE
    # ==========================================
    # PDF Requirement: Save engineered dataset
    print("[S] Serializing Output...")
    
    output_filename = 'thanos_housing_cleaned.csv'
    df.to_csv(output_filename, index=False)
    
    print("\n" + "="*50)
    print("   T.H.A.N.O.S. HOUSING REPORT COMPLETE")
    print("="*50)
    print(f"OUTPUT: {output_filename}")
    print(f"DATA INTEGRITY: {df.shape[0]} records processed.")
    print("="*50)

if __name__ == "__main__":
    run_housing_protocol()
