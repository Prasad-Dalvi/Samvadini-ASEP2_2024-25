import speech_recognition as sr
from googletrans import Translator
from TTS.api import TTS
import sounddevice as sd
import numpy as np

def recognize_translate_speak(target_lang="kn"):  # Use 'kn' for Kannada
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print(f"\n🎯 Target language: {target_lang.upper()}")
    print("🎤 Speak now... (Press Ctrl+C to stop)")

    translator = Translator()

    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        print("🔍 Recognizing...")
        input_text = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {input_text}")

        translated = translator.translate(input_text, dest=target_lang)
        print(f"🌐 Translated ({target_lang}): {translated.text}")

        print("🔊 Speaking out...")
        speak_text(translated.text, target_lang)

    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
    except sr.RequestError as e:
        print(f"⚠️ Could not request results; {e}")
    except Exception as ex:
        print(f"❗ Error: {ex}")

def speak_text(text, lang='kn'):
    try:
        # Load multilingual TTS model
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False, gpu=False)

        # Generate audio
        audio_array = tts.tts(text, speaker=tts.speakers[0], language=lang)

        # Play audio
        sd.play(audio_array, samplerate=22050)
        sd.wait()
    except Exception as e:
        print(f"❗ TTS error: {e}")

if __name__ == "__main__":
    recognize_translate_speak("kn")  # You can change 'kn' to 'hi', 'ta', 'bn', etc.