# sign_language_converter.py
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
import numpy as np

class SignLanguageSuggestor:
    def __init__(self):
        self.model = MultinomialNB()
        self.encoder = LabelEncoder()
        self.train()  # Train on sample data
        
    def train(self):
        # Features: [word_length, has_vowels]
        X = np.array([
            [5, 1],  # "hello"
            [3, 1],  # "cat"
            [6, 0],  # "symbol"
            [4, 1],  # "test"
        ])
        # Labels: difficulty levels
        y = ['easy', 'easy', 'hard', 'medium']
        self.encoder.fit(y)
        self.model.fit(X, self.encoder.transform(y))
        
    def predict_difficulty(self, text):
        features = np.array([[len(text), int(any(vowel in text.lower() for vowel in 'aeiou'))]])
        prediction = self.model.predict(features)
        return self.encoder.inverse_transform(prediction)[0]

sign_suggestor = SignLanguageSuggestor()

def audio_to_sign(text):
    difficulty = sign_suggestor.predict_difficulty(text)
    return f"Sign for '{text}' (Difficulty: {difficulty})"