import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# 1. Page Configuration (Mondial Style)
st.set_page_config(page_title="SkillQuery+ Dashboard", layout="wide")
st.title("🚀 SkillQuery+: 2026 Market Intelligence")
st.markdown("Compare your skills against 50,000+ global jobs and real Moroccan benchmarks.")

# 2. Load Data and Model
@st.cache_resource
def load_assets():
    df = pd.read_csv('data/skillquery_v2.csv')
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
    # Explode skills for counting
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



# 6. Geographic Distribution (Heatmap)
st.divider()
st.subheader("🌍 Global Job Density")

# Since our data has cities, we can plot a map
# Note: For a real map, we'd need Lat/Lon, but we can use a bubble chart for now
geo_data = df.groupby(['country', 'city']).size().reset_index(name='job_count')
fig_map = px.scatter_geo(geo_data, locations="country", locationmode='country names',
                         hover_name="city", size="job_count",
                         projection="natural earth", title="Market Hotspots")
st.plotly_chart(fig_map, use_container_width=True)