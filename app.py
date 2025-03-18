from flask import Flask, request, jsonify
import joblib
import os
import requests
import pandas as pd

app = Flask(__name__)

# 🔹 URL of the trained model stored in GitHub
MODEL_URL = "https://raw.githubusercontent.com/iamhabeebi/phishing/main/optimized_phishing_model.pkl"

# 🔹 Download the model from GitHub if not already present
if not os.path.exists("optimized_phishing_model.pkl"):
    print("Downloading model...")
    response = requests.get(MODEL_URL)
    with open("optimized_phishing_model.pkl", "wb") as f:
        f.write(response.content)
    print("✅ Model downloaded!")

# 🔹 Load the trained model
model = joblib.load("optimized_phishing_model.pkl")
print("✅ Model loaded successfully!")

# 🔹 Feature extraction function (modify based on your actual function)
def extract_features(url):
    return {
        "url_length": len(url),
        "https": 1 if url.startswith("https") else 0
    }

@app.route('/')
def home():
    return "Phishing Detection API is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get("url", "")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Extract features
    features = extract_features(url)
    feature_df = pd.DataFrame([features])

    # Make prediction
    prediction = model.predict(feature_df)[0]
    result = "Phishing" if prediction == 1 else "Legitimate"

    return jsonify({"url": url, "prediction": result})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
