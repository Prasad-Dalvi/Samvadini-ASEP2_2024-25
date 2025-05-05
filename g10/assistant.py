import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import pyjokes
import cohere
import requests

# Replace with your real Cohere API key
cohere_api_key = "yE1JizrCBl12Hv2NwkhfBx50fS91oL3QDwGUtZio"
co = cohere.Client(cohere_api_key)

weather_api_key = "eeb5d4ceaa630f202c303f7a13efa8f3"
city_name = "Pune"

r = sr.Recognizer()

def speak(command):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(command)
    engine.runAndWait()

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return f"The current temperature in {city_name} is {temp}°C with {description}."
    else:
        return "Sorry, I couldn't fetch the weather right now."

def get_cohere_response(prompt):
    try:
        response = co.chat(message=prompt, model="command-r")
        return response.text.strip()
    except Exception as e:
        return f"Cohere error: {e}"

def process_command_from_web(command):
    command = command.lower()

    if 'play' in command:
        song = command.replace('play', '').strip()
        pywhatkit.playonyt(song)
        return f"Playing {song}"

    elif 'how are you' in command:
        return "I'm doing great! Thanks for asking. What can I help you with?"

    elif 'date' in command:
        return str(datetime.date.today())

    elif 'time' in command:
        return datetime.datetime.now().strftime('%H:%M')

    elif 'weather' in command:
        return get_weather()

    elif "who is" in command or "what is" in command:
        person = command.replace('who is', '').replace('what is', '').strip()
        return wikipedia.summary(person, 1)

    elif 'joke' in command:
        return pyjokes.get_joke()

    elif 'ask ai' in command:
        prompt = command.replace('ask ai', '').strip()
        return get_cohere_response(prompt)

    else:
        return "Please ask a correct question."
