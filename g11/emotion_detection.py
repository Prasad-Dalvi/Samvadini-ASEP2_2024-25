# emotion_detection.py
from transformers import pipeline

# Load pre-trained emotion detection model
emotion_classifier = pipeline(
    "text-classification",
    model="bhadresh-savani/distilbert-base-uncased-emotion",
    return_all_scores=True
)

def detect_emotion(text):
    results = emotion_classifier(text)
    emotions = []
    
    # Process results and convert to our format
    for result in results[0]:
        emotions.append({
            "emotion": result["label"],
            "confidence": result["score"]
        })
    
    # Sort by confidence descending
    emotions.sort(key=lambda x: x["confidence"], reverse=True)
    
    # Add neutral if no strong emotion detected
    if emotions[0]["confidence"] < 0.4:
        emotions.insert(0, {
            "emotion": "neutral",
            "confidence": 1.0
        })
    
    return emotions[:3]  # Return top 3 emotions