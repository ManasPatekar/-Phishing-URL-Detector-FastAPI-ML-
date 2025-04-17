import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load dataset
df = pd.read_csv("F:/programs/python/phishing_detector/assets/PhiUSIIL_Phishing_URL_Dataset.csv")

# Clean and filter rows with NaN if any
df.dropna(inplace=True)

# Use all good numeric features except 'URL' and 'label'
X = df.drop(columns=['URL', 'label', 'Domain', 'TLD', 'Title'])  # Remove non-numeric columns
y = df['label']

# Convert any categorical values (like 'Yes'/'No') to binary
X = X.applymap(lambda x: 1 if x in ['Yes', 'yes', True] else (0 if x in ['No', 'no', False] else x))

# Ensure all values are numeric
X = X.apply(pd.to_numeric, errors='coerce').fillna(0)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
print("📊 Classification Report:")
print(classification_report(y_test, model.predict(X_test)))

# Save model
joblib.dump(model, "F:/programs/python/phishing_detector/model/phishing_model.pkl")
print("✅ Model trained and saved successfully!")
