import speech_recognition as sr
import pyttsx3
import webbrowser
import musicLibrary
from dotenv import load_dotenv
import os
import requests
from client import ai_process

load_dotenv()

api_key = os.getenv("news_api")

recognize = sr.Recognizer()

def commandProcess(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")

    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "open gmail" in c.lower():
        webbrowser.open("https://gmail.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        musicLibrary.search_and_play(song)

    elif "news" in c.lower():
        def fetch_top_headlines(api_key, country='us'):
            """
            Fetches top headlines from NewsAPI for a specified country.
            
            Args:
                api_key (str): Your NewsAPI key
                country (str): 2-letter country code (default: 'us')
            
            Returns:
                list: List of headline dictionaries or None if error occurs
            """
            url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}"
            
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raises HTTPError for bad responses
                data = response.json()
                
                if data['status'] == 'ok':
                    return data['articles']
                else:
                    print(f"API Error: {data.get('message', 'Unknown error')}")
                    return None
                    
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                return None

        # Usage
        headlines = fetch_top_headlines(api_key)

        if headlines:
            print(f"Found {len(headlines)} headlines:\n")
            for idx, article in enumerate(headlines, 1):
                headlines = f"{idx}. {article['title']}"
                speak(headlines)
                # print(f"   Source: {article['source']['name']}")
                # print(f"   URL: {article['url']}\n")
        else:
            print("Failed to fetch headlines.")

    elif c.lower().startswith("generate a code"):
        print("👩🏻‍💻Generating...")
        response = ai_process(c)
        with open("generated_code.py","w",encoding="utf-8") as f:
            f.write(response)
            
        speak("Your code has been generated. Opening file")
        os.system("start generated_code.py") 

    else:
        print("Processing...")
        response = ai_process(c)
        speak(response)

        

def speak(text):
    engine = pyttsx3.init() # initializing the engine each time because initializing it for once would ignore the voices after the first attempt.
    # engine.setProperty('rate', 150) # used to set frame to make speech a little slower. 
    engine.say(text)
    engine.runAndWait()
    

if __name__ == "__main__":
    speak("Initialiazing Jarvis")

    # wait till hears the word jarvis

    while True:
        # obtain audio from the microphone
        r = sr.Recognizer()
       
        print("Recognizing..")
    # recognize speech using Sphinx
        try:
             with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=2,phrase_time_limit=1.5)
                word = r.recognize_google(audio)

                if(word.lower() == "jarvis"):
                    
                    speak("Yeah")
                    with sr.Microphone() as source:
                        print("Jarvis Activated...")
                        audio = r.listen(source)
                        command = r.recognize_google(audio)
                        commandProcess(command)

                # print("Sphinx thinks you said " + r.recognize_sphinx(audio))
        except sr.UnknownValueError:
            print("Jarvis could not understand audio")
        except Exception as e:
            print("Error; {0}".format(e))