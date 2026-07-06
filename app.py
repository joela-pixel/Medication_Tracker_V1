import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime, date
import uuid

st.set_page_config(
    page_title="ADHD Med Tracker",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
CSV_PATH = DATA_DIR / "med_log.csv"

SYMP_RATINGS = ["No Impact", "Slightly Better", "Much Better", "Big Improvement"]
SIDE_EFFECTS = [
    "headache",
    "irritability",
    "constipation",
    "dizziness",
    "stomach-ache",
    "decreased appetite",
    "sweating",
    "shaking",
    "weight loss",
    "diarrhea",
    "nervousness",
    "increased heart rate",
    "difficulty sleeping",
]
EXERCISE_OPTIONS = ["10m", "20m", "30m", "more"]

FIELDS = [
    "entry_id",
    "date",
    "days_taken",
    "taken_time",
    "lasted_till",
    "dosage",
    "attention",
    "organization",
    "starting_tasks",
    "anxiety",
    "tired_0_10",
    "hunger_0_10",
    "sleep_0_10",
    "side_effects",
    "sleep_bedtime",
    "screen_time_end",
    "easy_sleep",
    "exercise",
    "anything_else",
    "week_notes",
    "status",
    "created_at",
]

def ensure_csv():
    if not CSV_PATH.exists():
        pd.DataFrame(columns=FIELDS).to_csv(CSV_PATH, index=False)

def load_data():
    ensure_csv()
    try:
        df = pd.read_csv(CSV_PATH)
    except Exception:
        return pd.DataFrame(columns=FIELDS)

    for col in FIELDS:
        if col not in df.columns:
            df[col] = ""

    if "entry_id" in df.columns:
        missing = df["entry_id"].astype(str).str.strip() == ""
        if missing.any():
            df.loc[missing, 
