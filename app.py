import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from sklearn.cluster import KMeans

# 1. Page Configuration (Mondial Style)
st.set_page_config(page_title="SkillQuery+ Dashboard", layout="wide")
st.title("🚀 SkillQuery+: 2026 Market Intelligence")
st.markdown("Compare your skills against 50,000+ global jobs and real Moroccan benchmarks.")

# 2. Load Data and Model
@st.cache_resource
def load_assets():
    df = pd.read_csv('data/skillquery_v2.csv')
    
    # --- FIX: DATA CLEANING (Prevents the NaN Error) ---
    # Fill empty salaries with the median and empty experience with 0
    df['salary_max_usd'] = df['salary_max_usd'].fillna(df['salary_max_usd'].median())
    df['min_experience_years'] = df['min_experience_years'].fillna(0)
    
    model = joblib.load('models/salary_model.pkl')
    encoders = joblib.load('models/encoders.pkl')
    return df, model, encoders

df, model, encoders = load_assets()

# 3. Sidebar - The "Query" Section
st.sidebar.header("🔍 Personal Career Query")
user_job = st.sidebar.selectbox("Target Role", encoders['job_title'].classes_)
user_country = st.sidebar.selectbox("Location", encoders['country'].classes_)
user_exp = st.sidebar.selectbox("Experience", encoders['experience_level'].classes_)

if st.sidebar.button("Predict My Salary"):
    t_idx = encoders['job_title'].transform([user_job])[0]
    c_idx = encoders['country'].transform([user_country])[0]
    e_idx = encoders['experience_level'].transform([user_exp])[0]
    
    prediction = model.predict([[t_idx, c_idx, e_idx]])[0]
    st.sidebar.success(f"Estimated Value: ${prediction:,.2f} USD")

# --- FEATURE 1: CAREER PATH SIMULATOR (In Sidebar) ---
st.sidebar.divider()
st.sidebar.header("🚀 Career Path Simulator")
sim_years = st.sidebar.slider("Simulate Years of Experience", 0, 15, 2)
sim_level = "Entry" if sim_years < 3 else "Mid" if sim_years < 7 else "Senior"
st.sidebar.info(f"At {sim_years} years, you are classified as: **{sim_level}**")

# 4. Main Dashboard - Visualizations
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Global vs. Local Salary")
    fig = px.bar(df[df['country'].isin(['Morocco', 'USA', 'UK', 'France'])], 
                 x='experience_level', y='salary_max_usd', color='country',
                 barmode='group', title="Salary Benchmarks")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🔥 Top 10 High-Demand Skills")
    all_skills = df['required_skills'].str.split(', ').explode()
    skill_counts = all_skills.value_counts().head(10)
    fig2 = px.pie(values=skill_counts.values, names=skill_counts.index, hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

# 5. The "Skill Gap" Feature
st.divider()
st.subheader("🎯 Skill Gap Analyzer")
my_skills = st.text_input("Enter your current skills (e.g., Python, Laravel, SQL)")
if my_skills:
    req_skills = set(df[df['job_title'] == user_job]['required_skills'].iloc[0].split(', '))
    user_set = set([s.strip() for s in my_skills.split(',')])
    missing = req_skills - user_set
    
    if missing:
        st.warning(f"To reach the {user_job} level, you should focus on: **{', '.join(missing)}**")
    else:
        st.balloons()
        st.success("You are a perfect match for this role!")

# --- FEATURE 2: REGIONAL HEATMAP (Morocco Hubs) ---
st.divider()
st.subheader("🇲🇦 Moroccan Tech Hubs")
ma_df = df[df['country'] == 'Morocco']
if not ma_df.empty:
    city_data = ma_df['city'].value_counts().reset_index()
    city_data.columns = ['City', 'Job Openings']
    fig_city = px.bar(city_data, x='City', y='Job Openings', color='City', 
                     title="Market Density by City", template="plotly_white")
    st.plotly_chart(fig_city, use_container_width=True)
else:
    st.info("Add more Moroccan entries to see the regional breakdown.")

# --- FEATURE 3: AI CLUSTERING (Job Grouping) ---
st.divider()
st.subheader("🧬 Job DNA Clustering")
st.write("Using K-Means AI to group roles with similar salary and experience requirements.")

# clustering
cluster_data = df[['salary_max_usd', 'min_experience_years']]
kmeans = KMeans(n_clusters=4, random_state=42)
df['Market_Cluster'] = kmeans.fit_predict(cluster_data)

fig_cluster = px.scatter(df, x="min_experience_years", y="salary_max_usd", 
                         color="Market_Cluster", hover_name="job_title",
                         title="AI Grouping: Salary vs Experience",
                         color_continuous_scale='Viridis')
st.plotly_chart(fig_cluster, use_container_width=True)