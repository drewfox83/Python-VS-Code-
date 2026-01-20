import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from math import pi 

# --- Configuration --- 
# Option 1: Enter your Spotify keys here if you have them. 
# Option 2: Leave as None to run in "Demo Mode" with mock data. 

CLIENT_ID = None # ex. 'your_long_random_string' 
CLIENT_SECRET = None # ex. 'your_other_long_random_string'

# --- 1. Data Fetching --- 
radar_data = {}
features_to_plot = ['danceability', 'energy', 'speechiness', 'acousticness', 'valence', 'tempo']

try: 
    if not CLIENT_ID or not CLIENT_SECRET: 
        raise ValueError("No keys found") 
    
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials

    # Authenticate 
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Real Playlists (You can swap these IDs for your own!) 
    playlists = {
        'Deep Focus (Coding)': '37i9QZF1DWZeKCadgRdKQ', 
        'Beast Mode (Gym)': '37i9dQZF1DX76Wlfdnj7AP', 
    }

    print("Connecting to Spotify API...") 
    for name, pid in playlists.items(): 
        results = sp.playlist_tracks(pid, limit=50)
        track_ids = [item['track']['id'] for item in results['items'] if item['track']]

        if not track_ids: continue 

        audio_features = sp.audio_features(track_ids)
        df = pd.DataFrame([f for f in audio_features if f]) # Filter out None

        # Normalize Tempo (divide by 200 to fit 0-1 scale) 
        if 'tempo' in df.columns: 
            df['tempo'] = df['tempo'] / 200.0 

        means = df[features_to_plot].mean().tolist()
        radar_data[name] = means

except Exception as e: 
    print(f"---> NOTICE: Running in Demo Mode (Reason: {e})") 
    # Fallback Data so you get a graph no matter what 
    radar_data = {
        'Deep Focus (Coding)': [0.55, 0.40, 0.10, 0.85, 0.30, 0.45], 
        'Beast Mode (Gym)':     [0.85, 0.95, 0.20, 0.05, 0.80, 0.90]
    }

# --- 2. Build RADAR CHART --- 
N = len(features_to_plot) 
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1] # Close the loop 

plt.figure(figsize=(8, 8))
ax = plt.subplot(111, polar=True) 

def add_radar_layer(data_list, color, label): 
    values = data_list
    values += values[:1] # Close the loop 
    ax.plot(angles, values, color=color, linewidth=2, label=label) 
    ax.fill(angles, values, color=color, alpha=0.25) 

# Plot Data 
add_radar_layer(radar_data['Deep Focus (Coding)'], '#3489db', 'Coding Mode')
add_radar_layer(radar_data['Beast Mode (Gym)'], '#e74c3c', 'Gym Mode')

# Formmating 
plt.xticks(angles[:-1], features_to_plot, size=10, color='black') 
ax.set_rlabel_position(0) 
plt.yticks([0.2, 0.4, 0.6, 0.8], ["20%", "40%", "60%", "80%"], color="grey", size=7) 
plt.ylim(0, 1) 

plt.title("Sonic Fingerprint: Playlist Analysis", y=1.08, fontsize=16, weight='bold') 
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

print("Radar Chart Generated successfully.") 
plt.show()