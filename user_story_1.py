import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data/processed_dataset.csv")

st.set_page_config(page_title="US1: School Admin Dashboard", layout="wide")

st.title("🏫 School Admin Dashboard - Filter & Monitor Students")

# === 1️⃣ Sidebar Filters ===
st.sidebar.header("🎛️ Filter")
grade = st.sidebar.selectbox("Grade", sorted(df['GradeID'].unique()))
subject = st.sidebar.selectbox("Subject", sorted(df['Topic'].unique()))

filtered_df = df[(df['GradeID'] == grade) & (df['Topic'] == subject)]

# === 2️⃣ Top Row: Key Metrics & Performance Chart ===
row1_col1, row1_col2 = st.columns([2, 1.5])  # wider metrics, narrower chart

with row1_col1:
    st.subheader(f"🎯 Overview (Grade {grade} | Subject {subject})")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    metric_col1.metric("Students", filtered_df.shape[0])
    metric_col2.metric("Avg. Raised Hands", round(filtered_df['raisedhands'].mean(), 1))
    metric_col3.metric("Avg. Visited Resources", round(filtered_df['VisITedResources'].mean(), 1))
    metric_col4.metric("Avg. Absence Days", round(filtered_df['StudentAbsenceDays'].mean(), 1))

with row1_col2:
    st.subheader("Performance Breakdown")
    fig1, ax1 = plt.subplots(figsize=(3, 2.5))
    sns.countplot(data=filtered_df, x='Class', order=['H', 'M', 'L'], palette='pastel', ax=ax1)
    ax1.set_xlabel("")
    ax1.set_ylabel("")
    ax1.set_title("")
    plt.tight_layout()
    st.pyplot(fig1, use_container_width=True)

# === 3️⃣ Bottom Row: At-Risk Table ===
st.subheader("🚩 At-Risk Students")

# Add an 'AtRisk' flag (simple rule)
filtered_df = filtered_df.copy()
filtered_df['AtRisk'] = (
    (filtered_df['raisedhands'] < filtered_df['raisedhands'].mean()) &
    (filtered_df['VisITedResources'] < filtered_df['VisITedResources'].mean()) &
    (filtered_df['StudentAbsenceDays'] > filtered_df['StudentAbsenceDays'].mean())
)

# Select key columns for display
show_df = filtered_df[['ID', 'GradeID', 'Topic', 'raisedhands', 'VisITedResources',
                       'StudentAbsenceDays', 'Class', 'AtRisk']]

# Limit table height to avoid scroll
st.dataframe(
    show_df.style.applymap(
        lambda val: 'background-color: salmon' if val == True else '',
        subset=['AtRisk']
    ),
    height=300  # control table height
)

st.info("✅ Tip: Red rows show at-risk students based on low engagement & high absences.")
