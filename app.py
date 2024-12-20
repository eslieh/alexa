# app.py
import random
import pywhatkit
import datetime
import wikipedia
from gtts import gTTS
import pygame
from actions import signup, login, get_contact, add_contact, log_action
from database import Session
import speech_recognition as sr
from models import User
import os
import requests
# Initialize Pygame
pygame.mixer.init()
sound_file = "wake.mp3"
listener = sr.Recognizer()
def say(text):
    """Convert text to speech using gTTS and play it."""
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")
        pygame.mixer.music.load("response.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        os.remove("response.mp3")
    except Exception as e:
        print(f"Error in TTS: {e}")

def play_sound():
    """Play a notification sound."""
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
def take_command(username, user_id):
        timeout=3
        wake_sound = ""  # Initialize 'command' to avoid UnboundLocalError
        try:
            with sr.Microphone() as source:
                print('Listening...')
                listener.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
                print("Listening for wake command...")
                voice = listener.listen(source, timeout=timeout, phrase_time_limit=4)  # Increase timeout and phrase time
                print("Processing...")
                wake_sound = listener.recognize_google(voice)
                wake_sound = wake_sound.lower()
                print(f'Command: {wake_sound}')
                run_alexa(wake_sound, username, user_id)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error: {e}")

def run_alexa(wake_sound, username, user_id):
    print("Waiting for wake-up command...")
    if "alexa" in wake_sound or "hey alexa" in wake_sound or "hello alexa" in wake_sound:
        print("I'm here!")
        number = random.randint(0, 2)
        if number == 1:
            play_sound()
        elif number == 2 :
            say(f"What's Up ,{username}")
        else:
            say("Hello there, how can I be of service?")
        take_request(username, user_id)

def take_request(username, user_id):
    query = ""
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)
            print("Listening for a command...")
            voice = listener.listen(source, timeout=6.5)
            print("Got it...")
            query = listener.recognize_google(voice)
            query = query.lower()
            print(f'Working on... {query}')
            process_alexa(query, username, user_id)
    except Exception as e:
        print(f"Error: {e}")

def process_alexa(query, username, user_id):
    if 'play' in query:
        song = query.replace('play', '').strip()
        say(f'Playing {song}')
        pywhatkit.playonyt(song)

    elif 'time' in query:
        time = datetime.datetime.now().strftime('%I:%M %p')
        say(f'Current time is {time}')
    elif 'who is' in query:
        person = query.replace('who is', '').strip()
        info = wikipedia.summary(person, 1)
        print(info)
        say(info)
    elif 'date' in query:
        current_date = datetime.datetime.now().strftime('%B %d, %Y')
        say(f"Today's date is {current_date}")
    elif 'weather' in query:
        city = query.replace('weather in', '').strip()
        weather_info = get_weather(city)
        say(weather_info)
    elif 'tell me a joke' in query:
        jokes = [
            "Why don’t scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don’t skeletons fight each other? They don’t have the guts."
        ]
        joke = random.choice(jokes)
        say(joke)
    elif 'send' in query and 'message' in query:
        try:
            # Extract contact name
            contact_name = query.replace('send a message to', '').strip().split(' ')[0]
            
            # Fetch the contact's phone number
            contact_exists, phone_number = get_contact(user_id, contact_name)
            
            if not contact_exists:
                phone_number = input(f"{contact_name} is not in your contacts. Enter their phone number: ")
                say(f"{contact_name} is not in your contacts. Enter their phone number: ")
                if phone_number:
                    add_contact(user_id, contact_name, phone_number)
                    say(f"{contact_name} has been added to your contacts.")
                else:
                    say("No phone number provided. Cannot send the message.")
                    return
            
            # Get the message content
            say(f'What do you want to tell {contact_name}?')
            with sr.Microphone() as source:
                listener.adjust_for_ambient_noise(source)
                print("Listening for the message...")
                voice = listener.listen(source, timeout=7.5)
                message = listener.recognize_google(voice)
                print(f"Message: {message}")
            
                # Send the message
                if message:
                    say(f'Sending message to {contact_name}: {message}')
                    pywhatkit.sendwhatmsg_instantly(phone_number, message)
                    log_action(user_id, 'send_message', f"To: {contact_name}, Message: {message}")
                else:
                    say("Sorry, I could not extract the message.")
        except Exception as e:
            say("Sorry, I could not send the message.")
            print(f"Error: {e}")

    elif 'news' in query:
        say("Fetching the latest news.")
        news = get_news()
        say(news)
    elif 'calculate' in query:
        try:
            calculation = query.replace('calculate', '').strip()
            result = eval(calculation)
            say(f'The result is {result}')
        except Exception:
            say("Sorry, I couldn't calculate that.")
    elif 'motivate me' in query:
        quotes = [
            "Believe you can and you're halfway there.",
            "Your limitation—it’s only your imagination.",
            "Push yourself, because no one else is going to do it for you."
        ]
        quote = random.choice(quotes)
        say(quote)
    elif 'set reminder' in query:
        say("What should I remind you about?")
        try:
            with sr.Microphone() as source:
                listener.adjust_for_ambient_noise(source)
                voice = listener.listen(source, timeout=5)
                reminder = listener.recognize_google(voice)
                say(f"Reminder set for: {reminder}")
        except Exception:
            say("Sorry, I couldn't catch the reminder.")
    elif 'trivia' in query:
        trivia_facts = [
            "Did you know? Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
            "Octopuses have three hearts.",
            "Bananas are berries, but strawberries aren’t!"
        ]
        fact = random.choice(trivia_facts)
        say(fact)
    else:
        say("I didn't catch that. Could you please repeat?")

def get_news():
    """Fetches the latest news headlines."""
    api_key = "96bb1def2547448c88e880166d92014b"  # Replace with your News API key
    url = f"https://newsapi.org/v2/top-headlines?country=ke&apiKey={api_key}"
    try:
        response = requests.get(url)
        articles = response.json()["articles"][:5]
        headlines = [article["title"] for article in articles]
        return "Here are the top headlines: " + ", ".join(headlines)
    except Exception as e:
        print(f"Error fetching news: {e}")
        return "I couldn't fetch the news at the moment."


def get_weather(city):
    """Fetch weather information for a city using OpenWeather API."""
    api_key = "410acbdb08992ef00d518f60ce7ea54b"  # Replace with your OpenWeather API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            return f"The weather in {city} is {weather} with a temperature of {temp}°C."
        else:
            return "I couldn't fetch the weather. Please check the city name."
    except Exception as e:
        print(f"Error: {e}")
        return "There was an error fetching the weather information."

def main():
    print("1. Signup")
    print("2. Login")
    choice = input("Choose an option (1 or 2): ")

    if choice == "1":
        username = input("Enter a username: ")
        name = input("Enter your name: ")
        password = input("Enter a password: ")
        success, user_id = signup(username, password, name)
        if success:
            print(f"Signup successful! Welcome, {name}.")
            say(f"Signup successful. Welcome, {name}.")
            # After signup, you could proceed with further actions
        else:
            print("Signup failed.")
    elif choice == "2":
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        success, username, user_id = login(username, password)
        if success:
            print(f"Login successful! Welcome back, {username}")
            say(f"Login successful! Welcome back, {username}")
            # Main app loop
            while True:
                take_command(username=username, user_id = user_id) 
            # After login, you could proceed with further actions
        else:
            print("Login failed.")
            say("Login failed.")
    else:
        print("Invalid choice.")
        say("Invalid choice. Please restart the app.")

# Main loop
if __name__ == "__main__":
    main()
