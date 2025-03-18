from flask import Flask, request, jsonify
import joblib
import os
import requests
import pandas as pd

app = Flask(__name__)

# 🔹 Replace this with your actual Google Drive file ID
FILE_ID = "https://drive.google.com/file/d/1-1hri-ZGccoVzjc2te46rZ0ypPtzkQFj/view?usp=sharing"
MODEL_PATH = "optimized_phishing_model.pkl"

# 🔹 Function to download the model from Google Drive
def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading model from Google Drive...")
        URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"
        response = requests.get(URL, stream=True)

        with open(MODEL_PATH, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print("✅ Model downloaded!")

# 🔹 Download model before starting the API
download_model()

# 🔹 Load the trained model
model = joblib.load(MODEL_PATH)
print("✅ Model loaded successfully!")

# 🔹 Dummy feature extraction function (replace with real logic)
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
