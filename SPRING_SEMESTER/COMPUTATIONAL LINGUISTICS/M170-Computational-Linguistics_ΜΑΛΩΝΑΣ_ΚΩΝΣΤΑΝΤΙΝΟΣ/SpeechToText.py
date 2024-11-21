import speech_recognition as sr
import webbrowser
import pyttsx3

def speak(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()


def obtain_audio_from_mic(message):
    # πάρε audio από το mic
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if message != None:
            speak(message)
        audio = r.listen(source)
    return audio


def convert_speech_to_text(audio):
    try:
        r = sr.Recognizer()
        query = r.recognize_google(audio, language="el-GR")
        return query
    except sr.UnknownValueError:
        return 0


def perform_google_search(query):
    # εκτέλεσε Google search
    url = "https://www.google.com/search?q=" + query
    webbrowser.open_new(url)
