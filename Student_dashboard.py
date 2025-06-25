import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data/processed_dataset.csv")

st.set_page_config(page_title="Student Dashboard", layout="wide")

st.title("📊 Student Performance Dashboard")

# === 1️⃣ General Overview ===
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", df.shape[0])
col2.metric("Grades", df['GradeID'].nunique())
col3.metric("Subjects", df['Topic'].nunique())
col4.metric("Performance Labels", df['Class'].nunique())

# === 2️⃣ Filters ===
st.markdown("### 🎯 Filter Students")
filter_col1, filter_col2 = st.columns(2)
selected_grade = filter_col1.selectbox("Select Grade", sorted(df['GradeID'].unique()))
selected_subject = filter_col2.selectbox("Select Subject", sorted(df['Topic'].unique()))
filtered_df = df[(df['GradeID'] == selected_grade) & (df['Topic'] == selected_subject)]
st.write(f"**Filtered students:** {filtered_df.shape[0]}")

# === 3️⃣ Insights Grid ===
st.markdown("### 📊 Insights")

# Smaller figsize & tighter arrangement
row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    st.caption("Engagement: Raised Hands vs Visited Resources")
    fig1, ax1 = plt.subplots(figsize=(3, 2.5))
    sns.scatterplot(data=filtered_df, x='raisedhands', y='VisITedResources', hue='Class', ax=ax1, s=30)
    ax1.set_xlabel("Raised Hands")
    ax1.set_ylabel("Visited Resources")
    ax1.set_title("")
    plt.tight_layout()
    st.pyplot(fig1, use_container_width=True)

with row1_col2:
    st.caption("Overall Class Distribution")
    fig2, ax2 = plt.subplots(figsize=(3, 2.5))
    sns.countplot(data=df, x='Class', order=df['Class'].value_counts().index, ax=ax2)
    ax2.set_xlabel("")
    ax2.set_ylabel("Count")
    ax2.set_title("")
    plt.tight_layout()
    st.pyplot(fig2, use_container_width=True)

with row1_col3:
    st.caption("Filtered Class Distribution")
    fig3, ax3 = plt.subplots(figsize=(3, 2.5))
    sns.countplot(data=filtered_df, x='Class', order=df['Class'].value_counts().index, ax=ax3)
    ax3.set_xlabel("")
    ax3.set_ylabel("Count")
    ax3.set_title("")
    plt.tight_layout()
    st.pyplot(fig3, use_container_width=True)

# Second row
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.caption("Absence Days by Class")
    fig4, ax4 = plt.subplots(figsize=(3, 2.5))
    sns.boxplot(data=df, x='Class', y='StudentAbsenceDays', ax=ax4)
    ax4.set_xlabel("")
    ax4.set_ylabel("Absence Days")
    ax4.set_title("")
    plt.tight_layout()
    st.pyplot(fig4, use_container_width=True)

with row2_col2:
    st.caption("Filtered Student Details")
    st.dataframe(filtered_df, height=250)

st.success("✅ Compact grid: easy to monitor trends quickly.")
