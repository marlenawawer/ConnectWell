from dotenv import load_dotenv
import os
from halo import Halo
from openai import OpenAI
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import speech_recognition as sr
import pyttsx3

load_dotenv(dotenv_path='.\constvar.env')
chat_history = []
chat_metadata = []
history_ids = []

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
    # Initialize the messages with a system message.
    chroma_client = chromadb.Client()
    embedding_function = OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_KEY"), model_name=os.getenv("EMBEDDING_MODEL"))
    collection = chroma_client.create_collection(name="conversations", embedding_function=embedding_function)
    current_id = 0
    messages=[{"role": "system", "content": "Hello. My name is Connect Well."}]
     
    speak_chat('Hello. My name is Connect Well.') 

    # Continue chatting
    while True:
        input_text = get_audio_mic()

        results = collection.query(query_texts=[input_text], 
                                   where={"role": "assistant"}, 
                                   n_results=2)
        
        for res in results['documents'][0]:
            messages.append({"role": "user", "content": f"previous chat: {res}"})

        # Add the user's message to the messages
        messages.append({"role": "user", "content": input_text})

        # Get a response from the model and add it to the messages
        response = generate_response(messages)

        chat_metadata.append({"role":"user"})
        chat_history.append(input_text)
        chat_metadata.append({"role":"assistant"})
        chat_history.append(response.content)
        current_id += 1
        history_ids.append(f"id_{current_id}")
        current_id += 1
        history_ids.append(f"id_{current_id}")
        collection.add(
            documents=chat_history,
            metadatas=chat_metadata,
            ids=history_ids)
        messages.append({"role": "system", "content": response.content})

        speak_chat(response.content)

        # Print the assistant's response
        # print(f"ConnectWell: {chat_history}")



if __name__ == "__main__":
    main()