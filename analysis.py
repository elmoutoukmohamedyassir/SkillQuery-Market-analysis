import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load the Combined Dataset
try:
    # We only load the columns we need to save RAM
    cols_to_use = ['job_title', 'country', 'experience_level', 'salary_max_usd', 'posted_year']
    df = pd.read_csv('data/skillquery_combined.csv', usecols=cols_to_use)
    print(" Combined Data loaded successfully!")
except FileNotFoundError:
    print(" Error: 'data/skillquery_combined.csv' not found. Run inject_local_data.py first!")
    exit()

# 2. Filter for Morocco vs Global
morocco_df = df[df['country'] == 'Morocco']
global_df = df[df['country'] != 'Morocco']

print(f"\n--- Market Analysis ---")
print(f"Total Global records: {len(global_df)}")
print(f"Total Morocco records: {len(morocco_df)}")

# 3. Calculate Average Salary by Experience (Global)
# This is a key insight for your portfolio
avg_salary_global = global_df.groupby('experience_level')['salary_max_usd'].mean().sort_values()
print("\n--- Average Global Max Salary (USD) ---")
print(avg_salary_global.apply(lambda x: f"${x:,.2f}"))

# 4. Visualization: Global vs Local Salary Trends
# We use Seaborn for that professional 'Mondial' look
plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")

# Create a comparison plot
sns.barplot(data=df, x='experience_level', y='salary_max_usd', hue='country', 
            palette='magma', errorbar=None)

plt.title('2026 Tech Salary Benchmark: Morocco vs. Global Average', fontsize=16, pad=20)
plt.xlabel('Experience Level', fontsize=12)
plt.ylabel('Annual Salary (USD)', fontsize=12)
plt.legend(title='Region')

# 5. Save the result
# Saving as an image is better for low-end PCs than plt.show()
plt.tight_layout()
plt.savefig('market_analysis_chart.png')
print("\n Analysis complete! Check 'market_analysis_chart.png' in your folder.")