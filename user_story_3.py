import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data/processed_dataset.csv")

st.set_page_config(page_title="US3: Policymaker Dashboard", layout="wide")

st.title("🏛️ Policymaker Dashboard: High-Level Student Trends")

# === 🎛️ Interactive Filters ===
st.sidebar.header("🎛️ Filters (Optional)")
grades = sorted(df['GradeID'].unique())
subjects = sorted(df['Topic'].unique())

selected_grade = st.sidebar.selectbox("Filter by Grade", ["All"] + grades)
selected_subject = st.sidebar.selectbox("Filter by Subject", ["All"] + subjects)

# Apply filters
filtered_df = df.copy()
if selected_grade != "All":
    filtered_df = filtered_df[filtered_df['GradeID'] == selected_grade]
if selected_subject != "All":
    filtered_df = filtered_df[filtered_df['Topic'] == selected_subject]

# === 📊 2x2 Grid ===
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# === 1️⃣ Overall Class Distribution ===
with row1_col1:
    st.subheader("Overall Performance Distribution")
    fig1, ax1 = plt.subplots(figsize=(3.5, 3))
    sns.countplot(data=filtered_df, x='Class', order=['H', 'M', 'L'], palette='Set2', ax=ax1)
    ax1.set_xlabel("")
    ax1.set_ylabel("Students")
    ax1.set_title("")
    st.pyplot(fig1, use_container_width=True)

# === ✅ Combined Bar + Line: Performance by Grade ===
with row1_col2:
    st.subheader("Performance by Grade (Bar + Line)")

    # Prepare data
    grade_perf = filtered_df.groupby(['GradeID', 'Class']).size().reset_index(name='Count')
    total_per_grade = grade_perf.groupby('GradeID')['Count'].sum().reset_index()
    total_per_grade.rename(columns={'Count': 'Total'}, inplace=True)
    grade_perf = pd.merge(grade_perf, total_per_grade, on='GradeID')
    grade_perf['Percentage'] = grade_perf['Count'] / grade_perf['Total'] * 100

    # Pivot to get High performance % trend
    trend_df = grade_perf[grade_perf['Class'] == 'H'][['GradeID', 'Percentage']].sort_values('GradeID')

    # Bar: total students by Grade & Class
    fig, ax1 = plt.subplots(figsize=(4.5, 3))
    sns.barplot(data=grade_perf, x='GradeID', y='Count', hue='Class', ax=ax1)
    ax1.set_xlabel("Grade")
    ax1.set_ylabel("Number of Students")

    # Line: High performance % trend
    ax2 = ax1.twinx()
    ax2.plot(trend_df['GradeID'], trend_df['Percentage'], color='black', marker='o', label='High Performance %')
    ax2.set_ylabel("High Performance (%)")
    ax2.set_ylim(0, 100)

    # Add legend for line
    ax2.legend(loc="upper right")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)


# === 3️⃣ Performance by Subject ===
with row2_col1:
    st.subheader("Performance by Subject")
    subject_perf = filtered_df.groupby(['Topic', 'Class']).size().reset_index(name='Count')
    fig3, ax3 = plt.subplots(figsize=(3.5, 3))
    sns.barplot(data=subject_perf, x='Topic', y='Count', hue='Class', ax=ax3)
    ax3.set_xlabel("Subject")
    ax3.set_ylabel("Students")
    ax3.set_title("")
    plt.xticks(rotation=45)
    st.pyplot(fig3, use_container_width=True)

# === 4️⃣ Absence vs Performance ===
with row2_col2:
    st.subheader("Absence Days vs Performance")
    fig4, ax4 = plt.subplots(figsize=(3.5, 3))
    sns.boxplot(data=filtered_df, x='Class', y='StudentAbsenceDays', order=['H', 'M', 'L'], ax=ax4)
    ax4.set_xlabel("Performance Class")
    ax4.set_ylabel("Absence Days")
    ax4.set_title("")
    st.pyplot(fig4, use_container_width=True)

# === ✅ Summary ===
st.success("✅ Interactive & compact: filter trends by grade/subject for policy decisions.")
