# train_emotion_model.py
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Enhanced single-word emotion dataset
data = {
    'text': [
        # Happy (40 words)
        'joy', 'happy', 'ecstatic', 'delighted', 'bliss', 'cheer', 'jubilant', 'elated',
        'thrilled', 'excited', 'gleeful', 'content', 'sunny', 'radiant', 'upbeat', 'lively',
        'vivacious', 'chipper', 'peppy', 'merry', 'festive', 'jovial', 'buoyant', 'exuberant',
        'optimistic', 'euphoric', 'grateful', 'playful', 'smiling', 'laughing', 'chirpy', 'glad',
        'blessed', 'fortunate', 'lucky', 'thankful', 'pleased', 'satisfied', 'triumphant', 'victorious',
        
        # Sad (40 words)
        'sad', 'gloomy', 'tearful', 'mournful', 'melancholy', 'depressed', 'miserable', 'sorrow',
        'heartbroken', 'despair', 'grief', 'woe', 'anguish', 'dismal', 'blue', 'downcast',
        'forlorn', 'glum', 'somber', 'morose', 'weepy', 'pained', 'hurt', 'dejected',
        'despondent', 'disheartened', 'crushed', 'defeated', 'lonely', 'isolated', 'abandoned', 'rejected',
        'unhappy', 'wretched', 'bereaved', 'pessimistic', 'hopeless', 'lost', 'empty', 'numb',
        
        # Angry (30 words)
        'angry', 'furious', 'enraged', 'irate', 'livid', 'incensed', 'outraged', 'seething',
        'hostile', 'annoyed', 'irritated', 'aggravated', 'vexed', 'resentful', 'indignant', 'infuriated',
        'cross', 'mad', 'heated', 'provoked', 'fuming', 'raging', 'storming', 'bitter',
        'spiteful', 'vengeful', 'grumpy', 'testy', 'snappy', 'cranky',
        
        # Fear (30 words)
        'afraid', 'scared', 'terrified', 'fearful', 'panicked', 'anxious', 'nervous', 'apprehensive',
        'worried', 'frightened', 'alarmed', 'horrified', 'petrified', 'shocked', 'startled', 'timid',
        'shaky', 'jittery', 'tense', 'uneasy', 'distressed', 'dread', 'phobic', 'paranoid',
        'threatened', 'vulnerable', 'intimidated', 'overwhelmed', 'hesitant', 'trembling',
        
        # Surprise (20 words)
        'surprised', 'shocked', 'amazed', 'astonished', 'stunned', 'flabbergasted', 'bewildered', 'dumbfounded',
        'speechless', 'startled', 'jolted', 'astounded', 'confounded', 'staggered', 'dazed', 'stupefied',
        'awestruck', 'thunderstruck', 'gobsmacked', 'perplexed',
        
        # Neutral (40 words)
        'okay', 'fine', 'neutral', 'normal', 'average', 'regular', 'usual', 'typical',
        'standard', 'mundane', 'routine', 'ordinary', 'common', 'plain', 'simple', 'moderate',
        'balanced', 'calm', 'steady', 'composed', 'collected', 'detached', 'impartial', 'objective',
        'unbiased', 'dispassionate', 'apathetic', 'indifferent', 'nonchalant', 'unemotional', 'stoic',
        'reserved', 'cool', 'measured', 'controlled', 'level', 'even', 'fair', 'moderate', 'middling'
    ],
    'emotion': (
        ['happy'] * 40 +
        ['sad'] * 40 +
        ['angry'] * 30 +
        ['fear'] * 30 +
        ['surprise'] * 20 +
        ['neutral'] * 40
    )
}

df = pd.DataFrame(data)

# Corrected model pipeline
model = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),  # Fixed syntax
    ('clf', SVC(
        kernel='rbf',
        C=1.5,
        gamma='scale', 
        probability=True
    ))
])

# Train the model
model.fit(df['text'], df['emotion'])

# Save the model
joblib.dump(model, 'emotion_model_single_word.pkl')

print("Model trained and saved successfully!")
print(f"Dataset contains {len(df)} training examples")
print("Class distribution:")
print(df['emotion'].value_counts())