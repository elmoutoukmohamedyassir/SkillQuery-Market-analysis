import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# 1. Load your V2 data
df = pd.read_csv('data/skillquery_v2.csv')

# 2. Encoding (Turning text into numbers)
# We save these encoders so we can use them later for new predictions
encoders = {}
for col in ['job_title', 'country', 'experience_level']:
    le = LabelEncoder()
    df[f'{col}_code'] = le.fit_transform(df[col])
    encoders[col] = le

# 3. Define Features (X) and Target (y)
X = df[['job_title_code', 'country_code', 'experience_level_code']]
y = df['salary_max_usd']

# 4. Split into Training and Testing sets (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Train the Random Forest
print(" Training the Salary Predictor (50,000 rows)...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Save the Model and Encoders for later use
joblib.dump(model, 'models/salary_model.pkl')
joblib.dump(encoders, 'models/encoders.pkl')

print(" Model trained and saved in 'models/' folder!")