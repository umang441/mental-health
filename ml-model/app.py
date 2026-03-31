from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# Constants
MODEL_PATH = 'model.pkl'
SCALER_PATH = 'scaler.pkl'
FEATURES = [
    'age', 'sex', 'agegroup', 'mstat', 'ses',
    'hltidx', 'hi_bp', 'arthp', 'blind', 'hearg',
    'smoke_do', 't_out', 't_indr', 't_rlx', 't_efft',
    'lonely', 'sleep', 'slpsev', 'insom'
]

# Load model and scaler
if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("✅ Model and Scaler loaded successfully.")
else:
    print("⚠️ Model or Scaler not found. Run train.py first.")

@app.route('/predict', methods=['POST'])
def predict():
    """
    POST endpoint to predict mental health status.
    Expected JSON input format:
    {
        "age": 65,
        "sex": 1,
        "agegroup": 2,
        ... all 19 features ...
    }
    """
    try:
        # 1. Get input data
        data = request.get_json(force=True)
        
        # 2. Extract features in order
        input_features = []
        for feature in FEATURES:
            if feature not in data:
                return jsonify({"error": f"Missing required feature: {feature}"}), 400
            input_features.append(data[feature])
            
        # 3. Convert to DataFrame and Scale
        input_df = pd.DataFrame([input_features], columns=FEATURES)
        input_scaled = scaler.transform(input_df)
        
        # 4. Predict
        prediction = int(model.predict(input_scaled)[0])
        # Bonus: Predict Probability (Confidence Score)
        probabilities = model.predict_proba(input_scaled)[0]
        confidence = float(np.max(probabilities))
        
        # 5. Return result
        return jsonify({
            "prediction": prediction,
            "confidence": round(confidence, 2)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return "🧠 Mental Health Prediction API is running!"

if __name__ == '__main__':
    # Change port if needed (default 5000)
    app.run(debug=True, port=5000)
