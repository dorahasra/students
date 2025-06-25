
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset
df = pd.read_csv("data/processed_dataset.csv")

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

# Title
st.title("📊 Student Performance Performance Dashboard")

# 1. Dataset Overview
st.header("1️⃣ Dataset Overview")
st.write("This dataset contains information about students' demographics and learning activities.")

col1, col2, col3 = st.columns(3)
col1.metric("Total Records", df.shape[0])
col2.metric("Total Features", df.shape[1])
col3.metric("Class Labels", df['Class'].nunique())

# 2. Class Distribution
st.header("2️⃣ Class Distribution")
fig1, ax1 = plt.subplots()
sns.countplot(data=df, x='Class', order=df['Class'].value_counts().index, ax=ax1)
ax1.set_title("Class Distribution (High, Medium, Low)")
st.pyplot(fig1)

# 3. Numerical Feature Summary
st.header("3️⃣ Numerical Features Summary")
st.dataframe(df.describe())

# 4. Correlation Heatmap
st.header("4️⃣ Feature Correlation Heatmap")
fig2, ax2 = plt.subplots(figsize=(12, 8))
numeric_df = df.select_dtypes(include='number')
sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax2)
ax2.set_title("Correlation Matrix")
st.pyplot(fig2)

# 5. Absence Days vs. Class
st.header("5️⃣ Absence Days vs. Class")
fig3, ax3 = plt.subplots()
sns.boxplot(data=df, x='Class', y='StudentAbsenceDays', ax=ax3)
ax3.set_title("Absence Days by Class")
st.pyplot(fig3)

# Footer
st.info("✅ This dashboard provides a quick snapshot of key trends to help you understand student behavior and performance.")
