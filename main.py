#This_is_Ruby_v1.0
#author_=_Avirup_Aditya
#Supports_Python_3.X_only


"""Written_in_Python 3.6
This application is currently under test and this version
is not the final release.
Ruby v1.0 - Your own personalized desktop assistant.
author = Avirup Aditya
reach out@avirup.aditya101@gmail.com
-----------------------------------------------------------
Last modified on 07/05/2019
"""


import pyttsx3
import webbrowser
import smtplib
import random
import speech_recognition as sr
import wikipedia
import datetime
import wolframalpha
import os
import sys
import requests
import re

engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices) - 1].id)


def speak(audio):
    print('Ruby: ' + audio)
    engine.say(audio)
    engine.runAndWait()


def timeSett():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        speak('Good Morning!')

    if currentH >= 12 and currentH < 18:
        speak('Good Afternoon!')

    if currentH >= 18 and currentH != 0:
        speak('Good Evening!')


timeSett()

speak('This is Ruby at your service!')
speak('How may I help you?')


def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio)
        print('User: ' + query + '\n')

    except sr.UnknownValueError:
        speak('Sorry! I didn\'t get that! Try typing the command!')
        query = str(input('Command: '))

    return query


if __name__ == '__main__':

    while True:

        query = myCommand()
        query = query.lower()

        if 'open youtube' in query:
            speak("okay! opening youtube...")
            webbrowser.open('www.youtube.com')

        elif 'open google' in query:
            speak('okay! opening google...')
            webbrowser.open('www.google.co.in')

        elif 'open gmail' in query:
            speak('okay! Opening your gmail...')
            webbrowser.open('www.gmail.com')

        elif "what\'s up" in query or 'how are you' in query:
            stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy']
            speak(random.choice(stMsgs))

        elif 'email' in query or 'mail' in query:
            speak('Who is the recipient? ')
            recipient = myCommand()

            if 'name_of_recipient' in recipient:
                try:
                    speak('What should I say? ')
                    content = myCommand()

                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.ehlo()
                    server.starttls()
                    server.login("your_email", "your_password")                 #fill your_email and your_password with your details
                    server.sendmail("recipient_mail", "your_mail", content)     #in place of name_of_recipient write the name you want to save
                    server.close()                                              #this code is for gmail accounts only if you have other mail accounts change the smtp port accordingly
                    speak('Email sent!')

                except:
                    speak('Sorry! I am unable to send your message at this moment!')


        elif 'nothing' in query or 'abort' in query or 'stop' in query:
            speak('okay')
            speak('Bye, have a good day.')
            sys.exit()

        elif 'hello' in query or 'hi' in query or 'hi Ruby' in query or 'hello Ruby' in query or 'hey Ruby' in query:
            speak('Hello there! How may I help you?')

        elif 'bye' in query:
            speak('Bye, have a good day.')
            sys.exit()

        elif 'play music' in query:
            music_folder = "music"
            music = ["music1", "music2", "music3", "music4", "music5"] #music 1,2,3,4,5 are the file names. 
            random_music = random.choice(music) + '.mp3'               #change it accordingly for your files
            os.system(random_music)                                    #also if you have music files in other folder specify the folder

            speak('Okay, here is your music! Enjoy!')

        elif 'joke' in query:
            res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept": "application/json"}
            )
            if res.status_code == requests.codes.ok:
                speak(str(res.json()['joke']))
            else:
                speak('oops!I ran out of jokes')

        elif "news" in query:
            my_url = " https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=9113b9445d8c4e399c473f41890d6126"
            my_open_bbc_page = requests.get(my_url).json()
            my_article = my_open_bbc_page["articles"]
            my_results = []
            for ar in my_article:
                my_results.append(ar["title"])
            speak("Here is the top ten headlines from BBC world.")
            for i in range(len(my_results)):
                print(i + 1)
                speak(my_results[i])


        elif 'open website' in query:

            reg_ex = re.search('open website (.+)', query)
            if reg_ex:
                domain = reg_ex.group(1)
                url = 'https://www.' + domain
                webbrowser.open(url)
                speak("Opening website...")
                speak('Done!')

            else:
                pass

        elif "search the web" in query:
            speak("Sure. What do you want to search?")
            search = myCommand()
            try:
                webbrowser.open('http://google.com/search?q=' + search)
            except:
                speak("Can't search at the moment! Check your internet connection.")
        else:
            query = query
            speak('Searching...')
            try:
                try:
                    client = wolframalpha.Client("A4VGW6-6YT3XAW3X5")
                    res = client.query(query)
                    results = next(res.results).text
                    speak('Got it! ')
                    speak(results)

                except:
                    results = wikipedia.summary(query, sentences=2)
                    speak('Got it!')
                    speak('Wikipedia says: ')
                    speak(results)

            except:
                speak('Sorry! can\'t search at the moment. Opening google... ')
                webbrowser.open('www.google.com')

        speak('Next Command!')


