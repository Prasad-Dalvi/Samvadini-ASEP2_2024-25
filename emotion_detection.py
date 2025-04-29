# emotion_detection.py
import joblib
import re
import numpy as np

# Load the trained model and TF-IDF vectorizer
model = joblib.load('emotion_model.pkl')

def detect_emotion(text):
    # Preprocess text
    cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
    
    # Predict emotion and confidence
    prediction = model.predict([cleaned_text])[0]
    probabilities = model.predict_proba([cleaned_text])
    confidence = np.max(probabilities)
    
    return {
        'emotion': prediction,
        'confidence': round(float(confidence), 2)
    }