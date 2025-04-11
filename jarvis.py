import pyttsx3  # type: ignore
import speech_recognition as sr  # type: ignore
import datetime
import wikipedia # type: ignore 
import webbrowser
import os
import subprocess  # This module allows us to run system-level commands like opening apps
import smtplib
from datetime import date


email = {
    "kaif":"mdkaif111967@gmail.com",
    "abrar nawaz":"abrarnawaz.az@gmail.com",
    "abdul rehaman" : "babdulrehamanbaig@gmail.com"
}

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id) # used to print which voice is used
engine.setProperty('voice', voices[0].id)  # for male voice -> voices[0].id and female voice -> voices[1].id

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour <= 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening")
    speak("I am Jarvis sir. please tell me how I may help you")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print("Listening....")
        r.adjust_for_ambient_noise(source, duration=3)
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        # r.pause_threshold = 0.8
        # audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")
    except Exception as e:
        print(e)
        say_again = "say that again please...."
        #speak(say_again)
        print(say_again)
        return "None"  # returning "None" string
    return query

#This function is used to send email
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com',5887)
    server.ehlo()
    server.starttls()
    server.login("mohammedkaif2474@gmail.com","your-password-here")
    server.sendmail("mohammedkaif2474@gmail.com",to,content)
    server.close()


if __name__ == '__main__':
    speak("hi")
    #wishMe()
    if 1:
        query = takecommand().lower()
        #Logic for excuting tasks based on query
        if 'wikipedia' in query:
            speak('Searching wikipedia....')
            query = query.replace('wikipedia',"")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open github' in query:
            webbrowser.open("https://github.com/Mohammedkaifuddin")

        #plays music
        elif 'play music' in query:
            music_dir = "C:\\Users\\name\\Music\\favourite_songs"
            songs = os.listdir(music_dir)
            print(songs,"\n")
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"kaif, The time is {strTime}")

        elif 'the date' in query:
            today_date = date.today()
            speak(f"kaif, today date is {today_date}")

        elif 'open vs code' in query:
            os.startfile("C:\\Users\\name\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")


        elif 'open whatsapp' in query:
            # whatsapp_path = "C:\\Program Files\\WindowsApps\\WhatsApp.exe"
            # os.startfile(whatsapp_path)
            #......
            # Open WhatsApp installed from the Microsoft Store
            # 'explorer' is the Windows File Explorer used to launch apps or files
            # 'shell:AppsFolder' is a special virtual folder that contains all installed apps (including Store apps)
            # '5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App' is WhatsApp's unique AppUserModelID (AUMID)
            # This ID is specific to WhatsApp installed via Microsoft Store and is required to launch it
            subprocess.Popen('explorer shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App')


        elif 'email to kaif' in query:
            try:
                speak("what should I say?")
                content = takecommand()
                to = "mdkaif111967@gmail.com"
                sendEmail(to,content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak(f"Sorry I am not able to the email to : {to}")


