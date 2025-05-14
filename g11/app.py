# app.py
from flask import Flask, request, jsonify, render_template
import pyttsx3
from emotion_detection import detect_emotion

app = Flask(__name__)

# Emotion to speech parameters mapping
EMOTION_PARAMS = {
    "joy": {"rate": 160, "volume": 1.0, "pitch": 120},
    "sadness": {"rate": 90, "volume": 0.7, "pitch": 80},
    "anger": {"rate": 200, "volume": 1.0, "pitch": 150},
    "fear": {"rate": 110, "volume": 0.6, "pitch": 90},
    "surprise": {"rate": 180, "volume": 0.9, "pitch": 130},
    "love": {"rate": 140, "volume": 0.95, "pitch": 110},
    "neutral": {"rate": 125, "volume": 0.85, "pitch": 100}
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/text-to-audio', methods=['POST'])
def text_to_audio():
    try:
        text = request.form['text'].strip()
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        emotions = detect_emotion(text)
        
        # Calculate weighted speech parameters
        total_weight = sum(e["confidence"] for e in emotions)
        speech_params = {
            "rate": 0,
            "volume": 0,
            "pitch": 0
        }
        
        for emotion in emotions:
            weight = emotion["confidence"] / total_weight
            params = EMOTION_PARAMS.get(
                emotion["emotion"], 
                EMOTION_PARAMS["neutral"]
            )
            for key in speech_params:
                speech_params[key] += params[key] * weight

        # Generate speech with adjusted parameters
        engine = pyttsx3.init()
        engine.setProperty('rate', int(speech_params["rate"]))
        engine.setProperty('volume', speech_params["volume"])
        
        try:  # Pitch setting might not be available on all systems
            engine.setProperty('pitch', int(speech_params["pitch"]))
        except:
            pass
        
        engine.say(text)
        engine.runAndWait()

        return jsonify({
            "status": "success",
            "emotions": emotions,
            "speech_params": speech_params,
            "text_length": len(text)
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)