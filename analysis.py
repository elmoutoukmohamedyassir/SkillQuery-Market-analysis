import pandas as pd

# 1. Load the dataset
# We use 'low_memory=True' to help your PC handle the file efficiently
try:
    df = pd.read_csv('data/ai_jobs.csv')
    print(" Data loaded successfully!")
except FileNotFoundError:
    print(" Error: 'ai_jobs.csv' not found in the /data folder.")

# 2. Basic Inspection
print("\n--- Project Overview (First 5 Rows) ---")
print(df.head())

print("\n--- Dataset Info ---")
# This shows you column names and if any data is missing
print(df.info())

print("\n--- Top 10 Job Titles Globally ---")
print(df['job_title'].value_counts().head(10))



# 3. Filter for Morocco 
# We check for 'MA' or 'Morocco' to be safe
morocco_jobs = df[df['country'].isin(['MA', 'Morocco', 'morocco', 'ma'])]

print("\n--- Morocco Market Snapshot ---")
if not morocco_jobs.empty:
    print(f" Total jobs found in Morocco: {len(morocco_jobs)}")
    print(morocco_jobs[['job_title', 'city', 'salary_max_usd', 'experience_level']].head(10))
else:
    print(" No jobs found for 'MA' or 'Morocco' in this dataset.")
    
    # Let's see what countries ARE in there so we can pick a backup
    print("\nTop 5 Countries in dataset:")
    print(df['country'].value_counts().head(5))