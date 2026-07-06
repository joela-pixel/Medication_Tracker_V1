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
        return df
    except Exception:
        return pd.DataFrame(columns=FIELDS)

def save_row(row):
    ensure_csv()
    df = pd.read_csv(CSV_PATH)
    row_df = pd.DataFrame([row])
    df = pd.concat([df, row_df], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)

def delete_entry(entry_id):
    ensure_csv()
    df = pd.read_csv(CSV_PATH)
    if "entry_id" in df.columns:
        df = df[df["entry_id"] != entry_id]
        df.to_csv(CSV_PATH, index=False)

def rating_widget(label, key):
    return st.radio(label, SYMP_RATINGS, horizontal=True, key=key, index=0)

def number_slider(label, key):
    return st.slider(label, 0, 10, 5, key=key)

st.markdown(
    """
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 5rem; max-width: 820px; }
    h1, h2, h3, p, label, div, span { font-size: 1.02rem; }
    .stButton button {
        width: 100%;
        padding: 0.85rem 1rem;
        border-radius: 14px;
        font-size: 1.05rem;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("💊 ADHD Medication Tracker")
st.caption("Mobile-first daily log based on your medication symptom tracker.")

tab1, tab2, tab3 = st.tabs(["Today", "History", "Export"])

with tab1:
    st.subheader("Daily log")
    with st.form("daily_log", clear_on_submit=False, enter_to_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            log_date = st.date_input("Date", value=date.today())
            dosage = st.text_input("Dosage", placeholder="Example: 10 mg")
            taken_time = st.text_input("Taken @", placeholder="Example: 8:00 AM")
        with c2:
            days_taken = st.multiselect(
                "Day(s) taken",
                ["M", "T", "W", "Th", "F", "Sa", "Su"],
                default=[],
            )
            lasted_till = st.text_input("Lasted till", placeholder="Example: 2:30 PM")
            easy_sleep = st.radio("Easy to fall asleep?", ["Yes", "No"], horizontal=True)

        st.markdown("### Effects")
        attention = rating_widget("Attention", "attention")
        organization = rating_widget("Organization", "organization")
        starting_tasks = rating_widget("Starting Tasks", "starting_tasks")
        anxiety = rating_widget("Anxiety", "anxiety")

        st.markdown("### Side effects")
        side_effects = st.multiselect("My side effects", SIDE_EFFECTS)

        st.markdown("### Body / energy")
        c3, c4, c5 = st.columns(3)
        with c3:
            tired = number_slider("Tired", "tired")
        with c4:
            hunger = number_slider("Hunger", "hunger")
        with c5:
            sleep = number_slider("Sleep", "sleep")

        st.markdown("### Sleep hygiene")
        c6, c7 = st.columns(2)
        with c6:
            sleep_bedtime = st.text_input("Bedtime", placeholder="Example: 11:30 PM")
        with c7:
            screen_time_end = st.text_input("Screen time end", placeholder="Example: 10:30 PM")

        exercise = st.radio("Exercise", EXERCISE_OPTIONS, horizontal=True)

        anything_else = st.text_area("Anything else?", placeholder="Notes about mood, stress, illness, travel, period, etc.")
        week_notes = st.text_area("Other important notes from this week", placeholder="Anything that may have affected how you felt that was not the medication.")
        status = st.radio("Entry status", ["Complete", "Incomplete"], horizontal=True, index=0)

        submitted = st.form_submit_button("Save entry")

    if submitted:
        row = {
            "entry_id": str(uuid.uuid4()),
            "date": str(log_date),
            "days_taken": ",".join(days_taken),
            "taken_time": taken_time,
            "lasted_till": lasted_till,
            "dosage": dosage,
            "attention": attention,
            "organization": organization,
            "starting_tasks": starting_tasks,
            "anxiety": anxiety,
            "tired_0_10": tired,
            "hunger_0_10": hunger,
            "sleep_0_10": sleep,
            "side_effects": ",".join(side_effects),
            "sleep_bedtime": sleep_bedtime,
            "screen_time_end": screen_time_end,
            "easy_sleep": easy_sleep,
            "exercise": exercise,
            "anything_else": anything_else,
            "week_notes": week_notes,
            "status": status,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        save_row(row)
        st.success("Saved.")

with tab2:
    st.subheader("History")
    df = load_data()
    if df.empty:
        st.info("No entries yet.")
    else:
        show_cols = [
            "date", "status", "dosage", "taken_time", "lasted_till",
            "attention", "organization", "starting_tasks", "anxiety",
            "tired_0_10", "hunger_0_10", "sleep_0_10", "side_effects"
        ]
        for col in show_cols:
            if col not in df.columns:
                df[col] = ""
        display_df = df[show_cols].copy()
        st.dataframe(display_df.sort_values("date", ascending=False), use_container_width=True, hide_index=True)

        st.markdown("### Delete entries")
        for _, row in df.sort_values("created_at", ascending=False).iterrows():
            with st.container(border=True):
                st.write(f"**Date:** {row.get('date','')} | **Dose:** {row.get('dosage','')} | **Status:** {row.get('status','')}")
                st.write(f"**Taken @:** {row.get('taken_time','')} | **Lasted till:** {row.get('lasted_till','')}")
                st.write(f"**Attention:** {row.get('attention','')} | **Organization:** {row.get('organization','')} | **Tasks:** {row.get('starting_tasks','')}")
                st.write(f"**Anxiety:** {row.get('anxiety','')} | **Side effects:** {row.get('side_effects','')}")
                confirm_key = f"confirm_delete_{row['entry_id']}"
                if st.button("Delete this entry", key=f"delete_{row['entry_id']}"):
                    st.session_state[confirm_key] = True
                if st.session_state.get(confirm_key, False):
                    st.warning("Tap confirm to permanently delete this entry.")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("Confirm delete", key=f"confirm_{row['entry_id']}"):
                            delete_entry(row["entry_id"])
                            st.session_state[confirm_key] = False
                            st.success("Entry deleted.")
                            st.rerun()
                    with col_b:
                        if st.button("Cancel", key=f"cancel_{row['entry_id']}"):
                            st.session_state[confirm_key] = False
                            st.rerun()

with tab3:
    st.subheader("Export")
    df = load_data()
    if df.empty:
        st.info("Nothing to export yet.")
    else:
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV",
            data=csv_data,
            file_name="adhd_med_tracker_log.csv",
            mime="text/csv",
            use_container_width=True,
        )
        st.markdown("### Summary")
        st.metric("Total entries", len(df))
        if "status" in df.columns:
            st.write(df["status"].value_counts())

st.caption("Use this app for personal tracking only. It does not replace medical advice.")
