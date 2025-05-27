import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

# Load dataset
df = pd.read_csv("C:\\Users\\yasha\\OneDrive\\Desktop\\ransomware_detector\\data\\ransomware_dataset.csv")

# Correct feature-target split
X = df.drop(columns=['is_malicious'])  # 12 features
y = df['is_malicious']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
model_path = os.path.join(os.path.dirname(__file__), 'ransomware_model.pkl')
joblib.dump(model, model_path)
print("Model trained and saved at:", model_path)

