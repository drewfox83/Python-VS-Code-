"""
Project: T.H.A.N.O.S. Titanic Protocol 
Description: Proprietary heuristic analysis system for the Titanic dataset. 
Author: T.H.A.N.O.S. Inc. 
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Configuration for optimized output
pd.set_option('display.max_columns', None)
sns.set_theme(style="whitegrid") 

def run_thanos_protocol(): 
    print(">>> Initializing T.H.A.N.O.S. Protocol...\n")

    # =======================
    # PHASE 1: [T] TAKE INGESTION
    # =======================
    print("[T] Taking Ingestion...")

    # Auto-detect local file or fetch from secure remote source
    file_path = 'titanic.csv'
    url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'

    if os.path.exists(file_path): 
        df = pd.read_csv(file_path)
        print("   Status: Local dataset loaded.")

    else:
        print( f"    Status: Local file missing. Fetching from remote source...") 
        df = pd.read_csv(url) 
    
    print(f" Dimensions: {df.shape[0]} rows, {df.shape[1]} columns")
    print("-" * 40) 

    # =======================
    # PHASE 2: [H] HEAL DATA
    # =======================
    print("[H] Healing Data...") 

    # Heuristic 1: Age (Median imputation for robustness) 
    missing_age = df['Age'].isnull().sum()
    df['Age'] = df['Age'].fillna(df['Age'].median())

    # Heuristic 2: Embarked (Mode Imputation) 
    missing_embarked = df['Embarked'].isnull().sum()
    if missing_embarked > 0: 
        df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
    
    # Heuristic 3: Cabin (Placeholder for augementation)
    df['Cabin']= df['Cabin'].fillna('Uknown') 

    print(f"   Repaired: {missing_age} Age values, {missing_embarked} Embarked values.")
    print("-" * 40)

    # =======================
    # PHASE 3: [A] AUGMENT FEATURES
    # =======================
    print("[A] Augmenting Features...") 

    # 1. HasCabin: Binary indicator of Wealth/Status
    df['HasCabin'] = df['Cabin'].apply(lambda x: 0 if x == 'Unknown' else 1)

    # 2. FamilySize: Aggregate social unit size. 
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1

    # 3. IsAlone: Isolation indicator
    df['IsAlone'] = df['FamilySize'].apply(lambda x: 1 if x == 1 else 0)

    # 4. AgeGroup: Demographic segmentation 
    bins = [0, 12, 19, 59, 120]
    labels = ['Child', 'Teen', 'Adult', 'Senior']
    df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels)

    print("    Generated: HasCabin, FamilySize, IsAlone, Agegroup")
    print("-" * 40) 

    # =======================
    # PHASE 4: [N] NARROW INSIGHYS (Visualization)
    # =======================
    print("[N] Narrowing Insights...") 

    # Setup visualization grid
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('T.H.A.N.O.S. Analysis: Survival Factors', fontsize=16) 

    # Visual 1 Gender
    sns.barplot(x='Sex', y='Survived', data=df, ax=axes[0], palette='viridis', ci=None)
    axes[0].set_title('Survival Rate by Gener') 

    # Visual 2: Economic Class 
    sns.barplot(x='Pclass', y='Survived', data=df, ax=axes[1], palette='magma', ci=None)
    axes[1].set_title('Survival Rate by Class')

    #Visual 3: Age Demographics 
    sns.barplot(x='AgeGroup', y='Survived', data=df, ax=axes[2], palette='cubehelix', ci=None) 
    axes[2].set_title('Survival Rate by Age Group') 

    plt.tight_layout()
    print("  Status: Charts generated. Launching interface...")
    plt.show()
    print("-" * 40)

    # =======================
    # PHASE 5: [0] OBSERVE STATISTICS
    # =======================
    print("[O] Observing Statistics...") 

    # Key Performance Indicators (KPIs) for Survival 
    gender_stats = df[['Sex', 'Survived']].groupby('Sex').mean()
    alone_stats = df[['IsAlone', 'Survived']].groupby('IsAlone').mean()
    class_stats = df[['Pclass', 'Survived']].groupby('Pclass').mean()

    # ======================
    # PHASE 6: [S] SERIALIZE & REPORT
    # =======================
    print("[S] Serializing Output...") 

    output_filename = 'thanos_titanic_cleaned.csv'
    df.to_csv(output_filename, index=False)

    # Final Report Generation 
    print("\n" + "="*50)
    print("    T.H.A.N.O.S. COMPREHENSIVE REPORT")
    print("="*50)
    print(f"STATUS: SUCCESS") 
    print(f"OUTPUT: {output_filename}") 
    print(f"\nCRITICAL FINDINGS:")
    print(f" > Female Survival:          {gender_stats.loc['female', 'Survived']:.1%}")
    print(f" > Male Survival:            {gender_stats.loc['male', 'Survived']:.1%}")
    print(f" > First Class Survival: {class_stats.loc[1, 'Survived']: 1%}")
    print(f" > Third Class Survival:  {class_stats.loc[3, 'Survived']:.1%}")
    print(f" > Solo Traveler Survival:{alone_stats.loc[1, 'Survived']:.1%}")
    print("="*50)

if __name__ == "__main__": 
    run_thanos_protocol()
    