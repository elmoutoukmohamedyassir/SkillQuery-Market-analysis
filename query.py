import joblib
import pandas as pd

# 1. Load the Model and the Encoders we saved during training
try:
    model = joblib.load('models/salary_model.pkl')
    encoders = joblib.load('models/encoders.pkl')
    print(" SkillQuery Engine Loaded Successfully.")
except FileNotFoundError:
    print("Error: Model files not found. Run train_model.py first!")
    exit()

def get_market_prediction(title, country, exp_level):
    try:
        # We must encode the user input exactly like we did during training
        title_encoded = encoders['job_title'].transform([title])[0]
        country_encoded = encoders['country'].transform([country])[0]
        exp_encoded = encoders['experience_level'].transform([exp_level])[0]
        
        # Create a tiny dataframe for the prediction
        input_data = pd.DataFrame([[title_encoded, country_encoded, exp_encoded]], 
                                   columns=['job_title_code', 'country_code', 'experience_level_code'])
        
        prediction = model.predict(input_data)[0]
        
        print(f"\n---  SkillQuery Prediction Result ---")
        print(f"Target Role: {title}")
        print(f"Location:    {country}")
        print(f"Experience:  {exp_level}")
        print(f"Predicted Salary: ${prediction:,.2f} USD")
        
    except ValueError as e:
        print(f"\n Prediction Error: One of your inputs is not in our 2026 intelligence base.")
        print(f"Available Countries: {list(encoders['country'].classes_[:5])}...")

# --- INTERACTIVE QUERY ---
if __name__ == "__main__":
    print("\n---  Welcome to SkillQuery+ Console ---")
    
    # Let's test it with a real-world Morocco scenario
    get_market_prediction("Data Scientist", "Morocco", "Junior")
    
    # Try a Global benchmark for comparison
    get_market_prediction("MLOps Engineer", "UK", "Senior")