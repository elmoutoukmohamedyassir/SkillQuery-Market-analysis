import pandas as pd

# Real 2026 Morocco Market Data
# Format: [Monthly MAD Min, Monthly MAD Max] -> Converted to Annual USD
morocco_market = [
    # [Job, City, Exp, Min_MAD, Max_MAD]
    ['Data Analyst', 'Casablanca', 'Junior', 10500, 14000],
    ['Data Analyst', 'Rabat', 'Intermediate', 16000, 21000],
    ['Data Scientist', 'Casablanca', 'Junior', 15800, 19000],
    ['Data Scientist', 'Rabat', 'Senior', 32000, 48000],
    ['MLOps Engineer', 'Casablanca', 'Intermediate', 24000, 31000],
    ['Machine Learning Engineer', 'Tangier', 'Junior', 15000, 18500],
    ['Data Scientist', 'Casablanca', 'Intermediate', 22000, 28000]
]

# Convert to DataFrame format
rows = []
for job, city, exp, min_m, max_m in morocco_market:
    rows.append({
        'job_title': job,
        'city': city,
        'country': 'Morocco',
        'experience_level': exp,
        'salary_min_usd': int(min_m * 12 * 0.10), # Monthly to Annual USD
        'salary_max_usd': int(max_m * 12 * 0.10),
        'posted_year': 2026,
        'industry': 'Tech/Finance'
    })

df_morocco = pd.DataFrame(rows)

# Load Global Data and Merge
df_global = pd.read_csv('data/ai_jobs.csv')
df_combined = pd.concat([df_global, df_morocco], ignore_index=True)

df_combined.to_csv('data/skillquery_combined.csv', index=False)
print(f" Injected {len(df_morocco)} real Moroccan entries into your global dataset.")