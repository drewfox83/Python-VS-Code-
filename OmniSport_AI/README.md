# ⚡ OmniSport AI: Real-Time Generative Sports Commentary

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?style=for-the-badge&logo=openai&logoColor=white)

## 📖 Project Overview
OmniSport AI is an automated sports broadcasting engine that ingests live game data and transforms it into real-time, persona-based commentary using Large Language Models (LLMs). 

Unlike static scoreboards, this system acts as an **AI Color Commentator**, capable of switching personalities (e.g., "The Hype Man" vs. "The Tactical Analyst") instantly to suit user preference.

### 🎯 Key Features
* **Real-Time Data Pipeline:** Simulates/Fetches live game states (Score, Clock, Momentum) for NBA and NFL.
* **Generative Narrative Engine:** Uses OpenAI's GPT models to generate context-aware commentary on the fly.
* **Dynamic Dashboard:** Built with Streamlit for sub-second latency updates.
* **Robust Error Handling:** Features a "Simulation Mode" fallback to ensure the demo never crashes, even without API connectivity.

---

## 🛠️ Technical Architecture

### The Pipeline
1.  **Ingestion:** Python scripts (`src/data_ingestion.py`) poll for live match data.
2.  **Processing:** Data is normalized into a standard JSON structure (Matchup, Score, Momentum).
3.  **Generation:** `src/ai_narrator.py` constructs a prompt based on the game state and selected Persona, sending it to the LLM.
4.  **Visualization:** Streamlit renders the dashboard, updating the DOM only where data has changed.

### The Stack
* **Language:** Python 3.10+
* **Frontend:** Streamlit
* **AI/ML:** OpenAI API (GPT-3.5/4)
* **Data Handling:** Pandas
* **Visualization:** Matplotlib / Seaborn

---

## 📊 Analytical Component
*Included as part of the Data Analyst Certification requirements.*

As part of the exploratory data analysis (EDA), I examined scoring volatility across different leagues to optimize the AI's "excitement" thresholds.

### Methodology
* **Dataset:** Simulated season data (n=100 games) for NBA and NFL.
* **Metric:** Total points scored per match.
* **Visualization:** Box-and-Whisker plots to analyze scoring distribution and outliers.

### Key Insights
1.  **Scoring Volume:** The NBA averages ~215 points/game compared to the NFL's ~45, requiring different scaling factors for the AI's "Hype" parameter.
2.  **Volatility:** NFL scores showed higher relative variance, suggesting that "scoring droughts" are more common and require different commentary filler strategies.

![Scoring Analysis Chart](notebooks/scoring_analysis.png)

---

## 🚀 How to Run Locally

**1. Clone the Repository**
```bash
git clone [https://github.com/YOUR_USERNAME/OmniSport_AI.git](https://github.com/YOUR_USERNAME/OmniSport_AI.git)
cd OmniSport_AI

# ⚡ OmniSport AI: Real-Time Generative Sports Commentary

OmniSport AI is a full-stack data application that transforms raw sports data into live, persona-based commentary using Generative AI.

## 🚀 The Vision
Most sports apps provide raw numbers. This project provides **narrative**. By combining real-time data ingestion with Large Language Models (LLMs), OmniSport AI acts as an automated "Color Commentator" for your favorite games.

## 🛠️ Technology Stack
* **Language:** Python 3.10+
* **Dashboard:** Streamlit (Real-time UI)
* **AI Brain:** OpenAI GPT-3.5/4 (Generative Logic)
* **Data Science:** Pandas, Matplotlib, Seaborn
* **Security:** Dotenv (API Key Management)

## 📊 Analytical Component (Capstone Requirement)
This project includes a dedicated analysis module (`notebooks/analysis_script.py`) that examines scoring volatility. 

**Key Insight:** By analyzing scoring spreads, we optimized the AI narrator to recognize "blowouts" vs. "nail-biters," ensuring the commentary matches the game's intensity.

![Scoring Analysis](notebooks/scoring_analysis.png)

## 📁 Project Structure
* `main_dashboard.py`: The live Streamlit application.
* `src/`: Core engine for data ingestion and AI narration.
* `notebooks/`: Exploratory data analysis and visualizations.
* `.env`: (Private) API credentials.

## 📝 License
This project is licensed under the MIT License - see the `LICENSE` file for details.