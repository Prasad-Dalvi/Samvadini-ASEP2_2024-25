# train_emotion_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
import joblib

# Sample dataset (expand with more examples)
data = {
    'text': [
        # Happy (8 examples)
        'I am thrilled with this wonderful news!',
        'What a fantastic surprise!',
        'This is the best day of my life!',
        'I feel ecstatic and overjoyed!',
        'Everything is going perfectly!',
        'You just made my day!',
        'I’m so grateful for this moment!',
        'This is absolutely amazing!',

        # Sad (8 examples)
        'Feeling gloomy and miserable today',
        'I feel anxious and worried',
        'This is the worst day ever',
        'I’m drowning in sadness',
        'Nothing seems to work out for me',
        'I feel utterly hopeless',
        'My heart is breaking into pieces',
        'The loneliness is crushing me',

        # Angry (6 examples)
        'This situation makes me furious',
        'I’m boiling with rage right now',
        'How dare you say that to me!',
        'This is completely unacceptable!',
        'I’ve never been so offended!',
        'You’re driving me crazy!',

        # Neutral (6 examples)
        'Neutral statement without strong emotion',
        'The meeting is scheduled for 3 PM',
        'Today’s weather is partly cloudy',
        'The document has been submitted',
        'Please update the spreadsheet',
        'The average temperature is 25°C',

        # Fear (4 examples)
        'I’m terrified of what might happen',
        'This uncertainty is frightening',
        'I feel a sense of impending doom',
        'My hands are shaking with fear',

        # Surprise (4 examples)
        'I can’t believe my eyes!',
        'This is completely unexpected!',
        'Wow, that took me by surprise!',
        'You just shocked me!'
    ],
    'emotion': [
        'happy', 'happy', 'happy', 'happy', 'happy', 'happy', 'happy', 'happy',
        'sad', 'sad', 'sad', 'sad', 'sad', 'sad', 'sad', 'sad',
        'angry', 'angry', 'angry', 'angry', 'angry', 'angry',
        'neutral', 'neutral', 'neutral', 'neutral', 'neutral', 'neutral',
        'fear', 'fear', 'fear', 'fear',
        'surprise', 'surprise', 'surprise', 'surprise'
    ]
}

df = pd.DataFrame(data)

# Define the ML pipeline
model = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('clf', SVC(kernel='linear', probability=True))
])

# Train the model
model.fit(df['text'], df['emotion'])

# Save the model
joblib.dump(model, 'emotion_model.pkl')