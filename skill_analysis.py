import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load the new V2 data
df = pd.read_csv('data/skillquery_v2.csv')

# 2. THE EXPLOSION: Turn "Python, SQL" into separate rows
# First, split the string into a list
df['skill_list'] = df['required_skills'].str.split(', ')

# Now, explode the list so each skill gets its own row
df_exploded = df.explode('skill_list')

# 3. Count the Frequency
top_skills = df_exploded['skill_list'].value_counts().head(10)

print("--- Top 10 Most Demanded Skills (Global + Morocco) ---")
print(top_skills)

# 4. Save the Visualization
plt.figure(figsize=(10, 6))
sns.barplot(x=top_skills.values, y=top_skills.index, palette='viridis')
plt.title('2026 Skill Demand: The "Mondial" Top 10', fontsize=14)
plt.xlabel('Number of Job Postings')
plt.savefig('top_skills_chart.png')
print(" Chart saved as 'top_skills_chart.png'")