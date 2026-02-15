# Automated Corporate Intelligence Pipeline 🕵️‍♂️📊

> **A resilient ETL and OSINT tool designed to automate high-value lead generation for corporate recruiting.**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-orange.svg)
![Status](https://img.shields.io/badge/Status-Active-green.svg)

## 📖 Overview
This project is a specialized **Data Engineering & Automation tool**. It solves a common business problem: manual research for corporate contacts is slow and error-prone.

This Python application ingests unstructured text data (job target lists), parses it into a structured database using **Regex**, and utilizes **"Grey Hat" Google Dorking** techniques to automatically retrieve LinkedIn profiles for key decision-makers.

Unlike simple scrapers, this tool is **fault-tolerant**, **state-aware**, and designed with **anti-detection logic** to operate safely without API keys.

## 🚀 Key Features
* **🔄 Unstructured Data ETL:** Custom Regex parser transforms messy raw text files (mixed headers, inconsistent delimiters) into clean, structured DataFrames.
* **🧠 Smart Resume Capability:** The script tracks its own progress. If stopped, crashed, or paused, it resumes *exactly* where it left off. Zero data loss.
* **🛡️ Anti-Bot Evasion:** Uses stochastic (randomized) delays (10-20s jitter) to mimic human browsing behavior and avoid Google's HTTP 429 blocks.
* **💾 Safety Checkpoints:** Automatically saves data every 5 records to prevent data loss during system interruptions.

## 🛠️ Tech Stack
* **Python 3.x**
* **Pandas** (Data manipulation & state management)
* **GoogleSearch-Python** (Search query automation)
* **OpenPyXL** (Excel I/O engine)
* **Regular Expressions** (Pattern matching & parsing)

## ⚙️ Installation

1.  **Clone the repo:**
    ```bash
    git clone