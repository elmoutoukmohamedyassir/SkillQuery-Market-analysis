import pandas as pd

# 1. Load the Combined Data
df = pd.read_csv('data/skillquery_combined.csv')

# 2. Define the "Skill Dictionary" (2026 Market Standards)
# This is what makes your project 'Smart'
skill_lookup = {
    'Data Scientist': 'Python, SQL, Machine Learning, Scikit-Learn, Statistics',
    'Data Analyst': 'SQL, Excel, Power BI, Python, Tableau',
    'MLOps Engineer': 'Docker, Kubernetes, CI/CD, Python, AWS, Terraform',
    'Machine Learning Engineer': 'Python, PyTorch, TensorFlow, FastAPI, MLOps',
    'AI Researcher': 'Python, PyTorch, NLP, Transformers, Research',
    'Applied Scientist': 'Python, SQL, Deep Learning, A/B Testing, Cloud'
}

# 3. Create the Logic to Map Skills
def get_skills(title):
    # Check if the title (or part of it) is in our dictionary
    for key in skill_lookup:
        if key.lower() in title.lower():
            return skill_lookup[key]
    return "Python, SQL, Problem Solving" # Default for unknown roles

# 4. Apply the mapping
df['required_skills'] = df['job_title'].apply(get_skills)

# 5. Save as a NEW version (v2)
df.to_csv('data/skillquery_v2.csv', index=False)
print("✅ Success! Your data now has a 'required_skills' column.")
print("Check the first few rows:")
print(df[['job_title', 'required_skills']].head())