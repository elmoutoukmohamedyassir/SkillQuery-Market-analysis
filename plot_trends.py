import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data/skillquery_combined.csv')

# Set the "Mondial" Style
plt.figure(figsize=(10, 6))
sns.set_theme(style="whitegrid")

# Create the Bar Plot
sns.barplot(data=df, x='experience_level', y='salary_max_usd', hue='experience_level', palette='viridis')

plt.title('Global Salary Benchmarks by Experience (2026)', fontsize=16)
plt.ylabel('Max Salary (USD)', fontsize=12)
plt.xlabel('Experience Level', fontsize=12)

# Save the plot so it doesn't just "pop up" and slow your PC
plt.savefig('salary_trends.png')
print("✅ Chart saved as 'salary_trends.png'. Open it to see the results!")