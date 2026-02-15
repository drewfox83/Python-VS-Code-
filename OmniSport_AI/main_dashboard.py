import streamlit as st
import time
import pandas as pd
from src.data_ingestion import SportsFetcher
from src.ai_narrator import AINarrator

# --- CONFIGURATION ---
st.set_page_config(page_title="OmniSport AI", page_icon="⚡", layout="wide")

# --- HEADER ---
st.title("⚡ OmniSport: Real-Time AI Commentary")
st.markdown("### The Future of Automated Sports Broadcasting")
st.divider()

# --- SIDEBAR ---
st.sidebar.header("🎛️ Control Panel")
sport = st.sidebar.selectbox("Select League", ["NBA", "NFL"])
persona = st.sidebar.selectbox("Select Personality", ["Hype Man", "Tactical Analyst", "Comedian"])

# --- ENGINES ---
fetcher = SportsFetcher()
narrator = AINarrator()

# --- MAIN FEED ---
if st.button("🔴 GO LIVE"):
    st.toast(f"Connecting to {sport} Data Stream...")
    
    # Create the placeholder
    dashboard = st.empty()
    
    # Run 10 updates
    for i in range(10):
        data = fetcher.fetch_live_data(sport)
        commentary = narrator.generate_commentary(data, persona)
        
        # USE THE PLACEHOLDER
        with dashboard.container():
            # Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Matchup", data.get('matchup', 'N/A'))
            col2.metric("Score", data.get('score', '0-0'))
            col3.metric("Clock", data.get('clock', '00:00'))
            
            # AI Box
            st.success(f"**AI Commentary:** {commentary}")
            
            # Data Table
            st.caption("Live Data Feed Log")
            st.dataframe(pd.DataFrame([data]))
            
        time.sleep(3)
        