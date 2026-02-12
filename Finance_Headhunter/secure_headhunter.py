import pandas as pd
from googlesearch import search
import time
import random
import re
import os
import sys

# --- CONFIGURATION ---
SOURCE_FILE = "job.data.csv"
DB_FILE = "Target_Database.xlsx"
SAVE_BATCH = 5  # Save every 5 rows to prevent data loss

def parse_source(filename):
    """
    ETL PHASE: Parses the raw text list into a structured DataFrame.
    Includes specific fix for "Smart Quotes" and mixed dashes.
    """
    data = []
    current_tier = "General"
    
    if not os.path.exists(filename):
        print(f"❌ Error: {filename} not found.")
        return []
        
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            # CLEANING: Remove smart quotes and extra spaces
            line = line.strip().replace('"', '').replace('”', '').replace('“', '')
            
            if not line: continue
            
            # 1. Detect Tier Headers
            if "TIER" in line.upper():
                if ":" in line:
                    current_tier = line.split(":")[0].strip()
                else:
                    current_tier = line.strip()
                continue
                
            # 2. Process Job Entries
            if "–" in line or "-" in line:
                try:
                    # Remove leading numbers (e.g. "1. ")
                    clean = re.sub(r'^\d+\.\s*', '', line)
                    
                    # Split by dash (handling both long and short dashes)
                    parts = re.split(r' – | - ', clean)
                    
                    if len(parts) >= 2:
                        # Extract Company & Location
                        comp_raw = parts[0]
                        company = comp_raw.split('(')[0].strip()
                        location = "South/Remote"
                        if "(" in comp_raw:
                            location = comp_raw.split('(')[-1].replace(')', '').strip()
                        
                        # Extract Role
                        role = parts[1].strip()
                        
                        # Extract Target Person (or default to Role)
                        target = role 
                        if len(parts) > 2:
                            target = parts[2].replace("Contact:", "").strip()
                        
                        data.append({
                            "Tier": current_tier,
                            "Company": company,
                            "Location": location,
                            "Role": role,
                            "Target_Person": target,
                            "LinkedIn_URL": "Pending"
                        })
                except Exception as e:
                    # Skip malformed lines
                    continue
    return data

def safe_save(df, filename):
    """Saves to Excel with error handling for open files."""
    try:
        df.to_excel(filename, index=False)
        return True
    except PermissionError:
        print(f"\n❌ LOCK ERROR: Please close '{filename}' in Excel! Retrying...")
        return False

def main():
    print("--- 🛡️ MASTER HEADHUNTER PIPELINE ACTIVE 🛡️ ---")
    
    # 1. LOAD OR INITIALIZE
    if os.path.exists(DB_FILE):
        print(f"📂 Database found. Resuming from previous session...")
        df = pd.read_excel(DB_FILE)
    else:
        print(f"🆕 Extracting data from {SOURCE_FILE}...")
        parsed_data = parse_source(SOURCE_FILE)
        
        if not parsed_data:
            print("❌ No data found! Check your CSV file content.")
            sys.exit()
            
        df = pd.DataFrame(parsed_data)
        safe_save(df, DB_FILE)
        print(f"✅ Successfully loaded {len(df)} targets.")

    # 2. IDENTIFY REMAINING WORK
    if 'LinkedIn_URL' not in df.columns:
        df['LinkedIn_URL'] = "Pending"
        
    pending_indices = df[df['LinkedIn_URL'] == "Pending"].index.tolist()
    print(f"⚡ {len(pending_indices)} searches remaining.")

    if not pending_indices:
        print("✅ All work complete!")
        return

    # 3. THE SEARCH LOOP
    for i, idx in enumerate(pending_indices):
        row = df.loc[idx]
        
        # Professional OSINT Search Query
        query = f'site:linkedin.com/in/ "{row["Company"]}" "{row["Target_Person"]}" "{row["Location"]}"'
        
        try:
            print(f"[{i+1}/{len(pending_indices)}] Searching: {row['Company']}...")
            
            # Randomized pause (10-15s) to stay safe
            results = list(search(query, stop=1, pause=random.uniform(10, 15)))
            
            if results:
                df.at[idx, 'LinkedIn_URL'] = results[0]
                print(f"   -> Found: {results[0]}")
            else:
                df.at[idx, 'LinkedIn_URL'] = "Not Found"
                print("   -> Not Found")
            
        except Exception as e:
            if "429" in str(e):
                print("⚠️  RATE LIMIT HIT: Pausing for 2 minutes...")
                time.sleep(120)
            else:
                print(f"⚠️ Error: {e}")
            continue

        # 4. DATA SECURITY (Save Checkpoint)
        if (i + 1) % SAVE_BATCH == 0:
            while not safe_save(df, DB_FILE):
                time.sleep(10) # Wait for user to close Excel
            print("💾 Progress saved.")
        
        # Jitter Delay
        time.sleep(random.uniform(5, 10))

    # Final Save
    safe_save(df, DB_FILE)
    print("\n🎉 BATCH COMPLETE. Results saved to Target_Database.xlsx")

if __name__ == "__main__":
    main()