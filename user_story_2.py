import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Load data
df = pd.read_csv("data/processed_dataset.csv")

st.set_page_config(page_title="US2: Teacher Performance Predictor", layout="wide")

st.title("👩‍🏫 Teacher Dashboard - Predict Student Performance")

# === 1️⃣ Prepare data ===
# Encode class labels
df = df.copy()
le = LabelEncoder()
df['Class_encoded'] = le.fit_transform(df['Class'])

# Features for prediction
features = ['raisedhands', 'VisITedResources', 'Discussion']

X = df[features]
y = df['Class_encoded']

# Train simple model (logistic regression)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# === 2️⃣ Teacher inputs ===
st.sidebar.header("🎛️ Set Engagement Levels")

raisedhands = st.sidebar.slider("Raised Hands", 0, int(df['raisedhands'].max()), 20)
visitedresources = st.sidebar.slider("Visited Resources", 0, int(df['VisITedResources'].max()), 20)
discussion = st.sidebar.slider("Discussion Participation", 0, int(df['Discussion'].max()), 10)

# === 3️⃣ Predict performance ===
input_df = pd.DataFrame({
    'raisedhands': [raisedhands],
    'VisITedResources': [visitedresources],
    'Discussion': [discussion]
})

pred = model.predict(input_df)[0]
pred_label = le.inverse_transform([pred])[0]

st.subheader("🎯 Predicted Class")
st.success(f"✅ **Predicted performance: {pred_label}**")

# === 4️⃣ Show sample actual data for comparison ===
st.subheader("📊 Sample Student Records")

sample_df = df.sample(10)[features + ['Class']]
st.dataframe(sample_df)

# === 5️⃣ Simple model performance ===
st.subheader("📈 Model Accuracy (Quick Check)")
accuracy = model.score(X_test, y_test)
st.write(f"Validation Accuracy: **{accuracy:.2%}**")
