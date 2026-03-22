import pandas as pd

# Load the V2 data
df = pd.read_csv('data/skillquery_v2.csv')

def analyze_skill_roi(target_job, my_skills_str, country="Morocco"):
    # 1. Filter data for the specific job and country
    market_data = df[(df['job_title'].str.contains(target_job, case=False)) & 
                     (df['country'] == country)]
    
    if market_data.empty:
        # Fallback to Global if Morocco data for that specific title is thin
        market_data = df[df['job_title'].str.contains(target_job, case=False)]
        print(f" Note: Using Global benchmarks for {target_job}")

    avg_salary = market_data['salary_max_usd'].mean()
    
    # 2. Clean and Compare Skills
    required_set = set(market_data.iloc[0]['required_skills'].split(', '))
    my_set = set([s.strip() for s in my_skills_str.split(',')])
    
    missing = required_set - my_set
    match_pct = (len(my_set.intersection(required_set)) / len(required_set)) * 100

    # 3. The "Power" Logic: Value per Skill
    # We estimate that each required skill contributes a portion of the total salary
    value_per_skill = avg_salary / len(required_set)

    print(f"\n---  SkillQuery ROI Report: {target_job} in {country} ---")
    print(f"Current Match: {match_pct:.1f}%")
    print(f"Target Salary: ${avg_salary:,.2f}")
    
    if missing:
        print("\n Skills to Acquire:")
        for skill in missing:
            print(f" + {skill} (Estimated Value: +${value_per_skill:,.2f}/year)")
    else:
        print("\n You match the full 2026 profile for this role!")

# --- TEST IT ---
# Let's say you are a dev in Morocco who knows Python but needs to bridge the gap
analyze_skill_roi("Data Scientist", "Python, Laravel", country="Morocco")