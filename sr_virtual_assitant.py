import os
import webbrowser
import speech_recognition as sr # type: ignore
from googletrans import Translator  # type: ignore # Ensure this is googletrans==4.0.0-rc1 or later
from textblob import TextBlob # type: ignore
from gtts import gTTS
import asyncio
import nest_asyncio
import platform

# Allow asyncio to run inside Jupyter/IPython
nest_asyncio.apply()

# Initialize recognizer and translator
recognizer = sr.Recognizer()
translator = Translator()

# Commands dictionary
commands = {
    "open browser": "Opening the web browser...",
    "open mail": "Opening the email client...",
    "open spotify": "Opening Spotify...",
}

# Function to open file in a cross-platform way
def open_file(filename):
    if platform.system() == "Windows":
        os.system(f"start {filename}")
    elif platform.system() == "Darwin":
        os.system(f"open {filename}")
    else:
        os.system(f"xdg-open {filename}")

# Function to recognize speech from the microphone
def recognize_speech_from_mic():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"Text: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Sorry, the service is down. Please try again later.")
            return None

# ✅ Updated speak function to avoid PermissionError
def speak(text, lang='en'):
    filename = "output.mp3"
    try:
        if os.path.exists(filename):
            os.remove(filename)
    except PermissionError:
        print("The audio file is in use. Please close it and try again.")
        return

    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    open_file(filename)

# Function to execute a command using keyword matching
def execute_command(command):
    command = command.lower()

    if "open browser" in command:
        print(commands["open browser"])
        webbrowser.open("http://www.google.com")

    elif "open mail" in command:
        print(commands["open mail"])
        os.system("start mailto:")

    elif "open spotify" in command:
        print("Opening Spotify...")
        os.system("start spotify")

    else:
        print("Command not recognized.")

# ✅ Updated to work in Jupyter/IPython with running event loop
def recognize_and_translate():
    async def do_translate(text):
        return await translator.translate(text, dest='hi')

    text = recognize_speech_from_mic()
    if text:
        loop = asyncio.get_event_loop()
        translated = loop.run_until_complete(do_translate(text))
        print(f"Translated Text (Hindi): {translated.text}")
        speak(translated.text, lang='hi')

# Function to analyze the sentiment of the recognized text
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        print("Positive sentiment detected!")
    elif sentiment < 0:
        print("Negative sentiment detected!")
    else:
        print("Neutral sentiment.")

# Continuous listening mode
def continuous_listen():
    print("Starting continuous listening mode... (Press Ctrl+C to stop)")
    listening = True
    while listening:
        try:
            text = recognize_speech_from_mic()
            if text:
                print(f"Recognized: {text}")
                execute_command(text)
        except KeyboardInterrupt:
            print("Stopping listening mode...")
            listening = False
        except Exception as e:
            print(f"An error occurred: {e}")

# Menu system to select options
def menu():
    while True:
        print("\nMenu:")
        print("1. Execute command")
        print("2. Translate speech (English to Hindi)")
        print("3. Analyze sentiment")
        print("4. Read back your speech")
        print("5. Exit")
        choice = input("Select an option (1-5): ")

        if choice == '1':
            text = recognize_speech_from_mic()
            if text:
                execute_command(text.lower())

        elif choice == '2':
            recognize_and_translate()

        elif choice == '3':
            text = recognize_speech_from_mic()
            if text:
                analyze_sentiment(text)

        elif choice == '4':
            print("Speak something to read it back...")
            text = recognize_speech_from_mic()
            if text:
                speak(text)

        elif choice == '5':
            print("Exiting...")
            break

        else:
            print("Invalid option. Please choose again.")

# Run the menu
menu()