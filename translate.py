import os
import time
import pygame
import streamlit as st
import speech_recognition as sr
from googletrans import LANGUAGES, Translator
import sounddevice as sd
from gtts import gTTS
st.set_page_config(page_title="Language Translator", page_icon=":globe_with_meridians:", layout="centered")
# Initialize global variables
isTranslateOn = False
translator = Translator()
pygame.mixer.init()

# Get language codes
language_mapping = {name: code for code, name in LANGUAGES.items()}

def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)

# Translate with error handling
def translator_function(spoken_text, from_language, to_language):
    try:
        return translator.translate(spoken_text, src=from_language, dest=to_language)
    except Exception as e:
        return f"Translation error: {e}"

# Text-to-voice with error handling
def text_to_voice(text_data, to_language):
    try:
        filename = f"cache_{time.time()}.mp3"
        voice_obj = gTTS(text=text_data, lang=to_language, slow=False)
        voice_obj.save(filename)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        os.remove(filename)
    except Exception as e:
        print(f"Text-to-voice error: {e}")

# Main translation process
def main_process(output_placeholder, from_language, to_language):
    global isTranslateOn
    while isTranslateOn:
        rec = sr.Recognizer()

        with sr.Microphone(device_index=4) as source:  # Replace '4' with the actual index
            output_placeholder.text("Listening...")
            rec.pause_threshold = 1
            audio = rec.listen(source, phrase_time_limit=10)

        try:
            output_placeholder.text("Processing...")
            spoken_text = rec.recognize_google(audio, language=from_language)

            output_placeholder.text("Translating...")
            translated_text = translator_function(spoken_text, from_language, to_language)
            output_placeholder.text(translated_text)

            text_to_voice(translated_text.text, to_language)
            time.sleep(3)

        except sr.UnknownValueError:
            output_placeholder.text("Could not understand audio")
        except sr.RequestError as e:
            output_placeholder.text(f"Could not request results from Google Speech Recognition service; {e}")

# Streamlit UI
st.title("Language Translator")

from_language_name = st.selectbox("Select Source Language:", list(LANGUAGES.values()))
to_language_name = st.selectbox("Select Target Language:", list(LANGUAGES.values()))
from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

start_button = st.button("Start")
stop_button = st.button("Stop")
output_placeholder = st.empty()

if start_button:
    if not isTranslateOn:
        isTranslateOn = True
        main_process(output_placeholder, from_language, to_language)

if stop_button:
    isTranslateOn = False