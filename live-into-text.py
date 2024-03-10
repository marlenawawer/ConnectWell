import speech_recognition as sr
import pyttsx3


r = sr.Recognizer()


def record_text(command):
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()

    while True:

        with sr.Microphone() as source:
            print('Listening...')
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source)

            input_text = r.recognize_whisper(audio)
            return input_text



def output_text(text):
    f = open('./output.txt', 'a')
    f.write(text)
    f.write('\n')
    f.close
    return

while True:
    text = record_text('start')
    output_text(text)

    print