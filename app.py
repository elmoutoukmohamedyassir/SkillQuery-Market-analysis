import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from sklearn.cluster import KMeans

# 1. Setup & Data Loading
st.set_page_config(page_title="SkillQuery+ Pro", layout="wide")
st.title("🇲🇦 SkillQuery+ Pro: 2026 Intelligence")

@st.cache_resource
def load_data():
    df = pd.read_csv('data/skillquery_v2.csv')
    model = joblib.load('models/salary_model.pkl')
    encoders = joblib.load('models/encoders.pkl')
    return df, model, encoders

df, model, encoders = load_data()

# --- FUNCTIONALITY 1: Career Path Simulator ---
st.sidebar.header("🚀 Career Path Simulator")
target_role = st.sidebar.selectbox("Dream Role", encoders['job_title'].classes_)
current_exp = st.sidebar.slider("Years of Experience", 0, 15, 2)

# Dynamic Prediction based on the slider
exp_label = "Entry" if current_exp < 3 else "Mid" if current_exp < 7 else "Senior"
t_idx = encoders['job_title'].transform([target_role])[0]
c_idx = encoders['country'].transform(["Morocco"])[0] # Default to Morocco for your local focus
e_idx = encoders['experience_level'].transform([exp_label])[0]

predicted_val = model.predict([[t_idx, c_idx, e_idx]])[0]
st.sidebar.metric(label=f"Predicted Salary ({exp_label})", value=f"${predicted_val:,.2f}")

# --- FUNCTIONALITY 2: Regional Heatmap (Morocco Focus) ---
st.header("📍 Moroccan Tech Hubs")
morocco_df = df[df['country'] == 'Morocco']
if not morocco_df.empty:
    city_counts = morocco_df['city'].value_counts().reset_index()
    city_counts.columns = ['city', 'jobs']
    
    # We use a Pie or Bar for city density since we lack Lat/Lon for a precise map
    fig_city = px.bar(city_counts, x='city', y='jobs', color='city', 
                     title="Job Density by Moroccan City", template="plotly_dark")
    st.plotly_chart(fig_city, use_container_width=True)
else:
    st.info("Inject more Morocco data to see the city breakdown!")

# --- FUNCTIONALITY 3: Job Clustering (The 'Famous' Feature) ---
st.divider()
st.header("🧬 Job & Skill Clustering")
st.write("This AI groups jobs that share similar 'DNA' (Salary + Experience + Skills).")

# Prepare data for Clustering
cluster_df = df[['salary_max_usd', 'min_experience_years']].copy()
kmeans = KMeans(n_clusters=4, random_state=42).fit(cluster_df)
df['cluster'] = kmeans.labels_

# Visualizing the Clusters
fig_cluster = px.scatter(df, x="min_experience_years", y="salary_max_usd", 
                         color="cluster", hover_name="job_title",
                         title="AI Clustering: Finding Your 'Neighbor' Roles",
                         labels={"cluster": "Job Group"},
                         template="plotly_white")
st.plotly_chart(fig_cluster, use_container_width=True)

st.info("💡 Insight: Roles in the same color share similar career trajectories.")