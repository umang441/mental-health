import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

# 1. Define Features and Target
FEATURES = [
    'age', 'sex', 'agegroup', 'mstat', 'ses',
    'hltidx', 'hi_bp', 'arthp', 'blind', 'hearg',
    'smoke_do', 't_out', 't_indr', 't_rlx', 't_efft',
    'lonely', 'sleep', 'slpsev', 'insom'
]
TARGET = 'psych_85'

def train_model(data_path='mental_health_data.csv'):
    # Check if dataset exists
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Please provide a dataset.")
        return

    # Load Dataset
    print(f"Loading dataset from {data_path}...")
    df = pd.read_csv(data_path)

    # 2. Data Preprocessing
    # Handle missing values (fill numerical with median, categorical with mode)
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].median())

    # Encode categorical variables if they aren't already numerical
    # We'll collect encoders if needed, but for simplicity in this module we'll assume basic encoding
    for col in df.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])

    # Select Features and Target
    X = df[FEATURES]
    y = df[TARGET]

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Scaling
    print("Normalizing features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Save Scaler
    joblib.dump(scaler, 'scaler.pkl')
    print("✅ Scaler saved as scaler.pkl")

    # 4. Train Model
    print("Training RandomForestClassifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    # Evaluate
    predictions = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, predictions)
    print(f"✅ Accuracy: {accuracy * 100:.2f}%")

    # 5. Save Model
    joblib.dump(model, 'model.pkl')
    print("✅ Model saved as model.pkl")

if __name__ == "__main__":
    train_model()
