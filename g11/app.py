from flask import Flask, request, jsonify, render_template
import pyttsx3
from emotion_detection import detect_emotion

# Initialize Flask app
app = Flask(__name__)

# Home route - serves HTML form
@app.route('/')
def home():
    return render_template('index.html')

# Text-to-audio conversion endpoint
@app.route('/text-to-audio', methods=['POST'])
def text_to_audio():
    try:
        # Get and validate input text
        text = request.form['text'].strip()
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Detect emotion
        emotion_data = detect_emotion(text)
        emotion = emotion_data['emotion']
        confidence = emotion_data['confidence']

        # Convert text to speech with emotion-adjusted settings
        engine = pyttsx3.init()
        
        # Adjust speech parameters based on emotion
        if emotion == 'happy':
            engine.setProperty('rate', 150)  # Faster speech for happiness
            engine.setProperty('volume', 1.0)
        elif emotion == 'sad':
            engine.setProperty('rate', 100)  # Slower speech for sadness
            engine.setProperty('volume', 0.8)
        else:  # neutral/other
            engine.setProperty('rate', 125)
            engine.setProperty('volume', 0.9)
            
        engine.say(text)
        engine.runAndWait()

        # Return results
        return jsonify({
            'status': 'success',
            'message': f'Converted to audio with {emotion} emotion',
            'emotion': emotion,
            'confidence': float(confidence),
            'text_length': len(text)
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Run the application
if __name__ == '__main__':
    app.run(debug=True, port=5000)