import speech_recognition as sr
import pyttsx3
import sqlite3
import pywhatkit
import wikipedia
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configure Text-to-Speech Engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Change index to select different voice

# Speak Function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Take Command Function
def takeCommand():
    """
    Takes microphone input from the user and returns it as text.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("Unable to Recognize your voice.", e)
        return "None"

    return query

# Wish Me Function
def wishMe():
    """
    Greets the user based on the current time.
    """
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am your assistant. How may I help you?")

# Database Functions
def create_user_table():
    """
    Creates a table in the SQLite database to store user preferences.
    """
    conn = sqlite3.connect('database/database/user_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        wake_up_word TEXT
                    )''')
    conn.commit()
    conn.close()

def add_user(name, wake_up_word):
    """
    Adds a new user to the database.
    """
    conn = sqlite3.connect('database/database/user_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, wake_up_word) VALUES (?, ?)", (name, wake_up_word))
    conn.commit()
    conn.close()

def get_wake_up_word(user_id):
    """
    Retrieves the wake-up word for a specific user.
    """
    conn = sqlite3.connect('database/user_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT wake_up_word FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

# Selenium Functions
def setup_driver():
    """
    Sets up the Selenium WebDriver.
    """
    try:
        driver = webdriver.Chrome(executable_path="./chromedriver")  # Replace with your path
        driver.maximize_window()
        return driver
    except Exception as e:
        print(f"Error setting up Selenium WebDriver: {e}")
        return None

def open_youtube(driver):
    try:
        driver.get("https://www.youtube.com")
        speak("Opening YouTube.")
    except Exception as e:
        print(f"Error opening YouTube: {e}")
        speak("I encountered an issue while opening YouTube.")

def open_google(driver):
    try:
        driver.get("https://www.google.com")
        speak("Opening Google.")
    except Exception as e:
        print(f"Error opening Google: {e}")
        speak("I encountered an issue while opening Google.")

def search_youtube(driver, song):
    try:
        driver.get("https://www.youtube.com")
        search_box = driver.find_element(By.NAME, "search_query")
        search_box.send_keys(song)
        search_box.send_keys(Keys.RETURN)
        speak(f"Searching for {song} on YouTube.")
    except Exception as e:
        print(f"Error searching YouTube: {e}")
        speak("I encountered an issue while searching YouTube.")

# Main Function
if __name__ == "__main__":
    create_user_table()  # Create the user table if it doesn't exist

    # Example: Add a new user (only run once to populate the database)
    add_user("John Doe", "Hey Siri")

    # Get the wake-up word for the user (replace with actual user ID)
    user_id = 1  # Example user ID
    wake_up_word = get_wake_up_word(user_id)

    # Set up Selenium WebDriver
    driver = setup_driver()

    if wake_up_word and driver:
        wishMe()
        while True:
            query = takeCommand().lower()

            if query == 'none':
                continue

            if wake_up_word in query:
                query = query.replace(wake_up_word, "")

            if 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                try:
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)
                except Exception as e:
                    print(f"Error fetching Wikipedia data: {e}")
                    speak("I couldn't find any information on that topic.")

            elif 'open youtube' in query:
                open_youtube(driver)

            elif 'open google' in query:
                open_google(driver)

            elif 'play music on youtube' in query:
                song = query.replace('play music on youtube', '')
                search_youtube(driver, song)

            elif 'send message' in query:
                try:
                    phone_no = input("Enter the phone number: ")
                    message = input("Enter the message: ")
                    pywhatkit.sendwhatmsg(phone_no, message, datetime.datetime.now().hour, datetime.datetime.now().minute + 2)
                    speak("Message sent successfully!")
                except Exception as e:
                    print(f"Error sending WhatsApp message: {e}")
                    speak("I couldn't send the message.")

            elif 'quit' in query:
                speak("Quitting.")
                driver.quit()  # Close the browser
                break
