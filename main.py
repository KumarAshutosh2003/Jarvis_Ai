import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import winsound
import MusicLibrary
import client
import requests

# Creating the recogniser

r = sr.Recognizer()
newsapi = "c947759930774b358e3e2fb102356b76"

def speak(text):
    engine = pyttsx3.init()   # creating new engine every time
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# Normal Accessing Functions

def process_cmd(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = MusicLibrary.music[song]
        webbrowser.open(link)
    # To get the news
    
    elif "news" in c.lower():
        speak("Fetching latest news")
        r = requests.get(f"https://newsapi.org/v2/everything?q=india&sortBy=publishedAt&language=en&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', []) 

            if not articles:
                speak("Sorry, I could not find any news.")
                return

            speak("Here are the top headlines")

            for article in articles[:5]:  # First 5 news headlines
                title = article.get("title")
                if title:
                    print(title)
                    speak(title)
                    time.sleep(1)

    else: # Rest function with ai client
        speak("Let me think")
        ai_response = client.ask_ai(c)
        print("AI:", ai_response)
        speak(ai_response)

if __name__ == "__main__":
    speak("Initialising Jarvis......")
    while True:
        ## Old code for testing the speech recognition
        # obtain audio from the microphone
        # with sr.Microphone() as source:
        #     print("Listening...")
        #     audio = r.listen(source, timeout=5, phrase_time_limit = 3)
        #     word = r.recognize_google(audio)
        
        # recognize speech using Google audio
        # print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit = 3)
            word = r.recognize_google(audio)
            print(word)

            if "jarvis" in word.lower():
                print("DEBUG: Wake word detected") # Just to see if the code is running or not
                speak("Hello Sir , How can I help you ?")
                time.sleep(1.2)
                print("Jarvis is Activated")
                print("give command")

                #listen for the command 
                with sr.Microphone() as source:
                    print("give command")
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    command = r.recognize_google(audio)
                    process_cmd(command)


        except sr.UnknownValueError:
            print("Could not understand")
        except Exception as e:
            print("Error; {0}".format(e))
