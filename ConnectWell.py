from dotenv import load_dotenv
import os
from halo import Halo
from openai import OpenAI
import speech_recognition as sr
import pyttsx3
import streamlit as st
import time

load_dotenv(dotenv_path='.\constvar.env')

def generate_response(messages):
    # Create a loading spinner
    spinner = Halo(text='Loading...', spinner='dots')
    spinner.start()

    client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
    model_name = os.getenv("MODEL_NAME")

    # Create a chat completion with the provided messages
    response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.5,
            max_tokens=250)

    # Stop the spinner once the response is received
    spinner.stop()

    # Return the message part of the response
    return response.choices[0].message

def speak_chat(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text) 
    engine.runAndWait()

def get_audio_mic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
        text = r.recognize_whisper(audio)
        return text


def main():    
    st.title("ConnectWell")
    messages=[{"role": "system", "content": "Hello. My name is Connect Well."}]
    start = st.toggle('Slide right to start chatting')
    if start:
        window = st.container(height=300)
        window.chat_message("assistant").write('Hello. My name is Connect Well.')
        speak_chat('Hello. My name is Connect Well.') 
        while True:
            plakceholder = st.empty()
            plakceholder.text("Recording started.")
            input_text = get_audio_mic()
            plakceholder.empty()
            window.chat_message("user").write(f"{input_text}")
            messages.append({"role": "user", "content": input_text})

            # Get a response from the model and add it to the messages
            response = generate_response(messages)

            messages.append({"role": "system", "content": response.content})
            window.chat_message("assistant").write(f'{response.content}')
            speak_chat(response.content)
    else:
        st.stop()

if __name__ == "__main__":
    main()
