import speech_recognition as sr
import os
import pygame
import pywhatkit
import datetime
import wikipedia
import random
# Initialize Pygame mixer to play sound notifications
pygame.mixer.init()

# Path to your sound file (replace with your own sound file)
sound_file = "wake.mp3"

def say(text):
    os.system(f'echo "{text}" | festival --tts')

def play_sound():
    pygame.mixer.music.load(sound_file)  # Load the sound file
    pygame.mixer.music.play()  # Play the sound
    while pygame.mixer.music.get_busy():  # Wait until the sound finishes playing
        continue

listener = sr.Recognizer()

def take_command(timeout= 7):
    wake_sound = ""  # Initialize 'command' to avoid UnboundLocalError
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source)  # Adjust for ambient noise levels
            print("Listening for wake command...")
            voice = listener.listen(source, timeout=timeout)  # Listen for command
            print("alexa initialised")
            wake_sound = listener.recognize_google(voice)
            wake_sound = wake_sound.lower()
            print(f'Command: {wake_sound}')
            run_alexa(wake_sound)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"Error: {e}")

def run_alexa(wake_sound):
    print("Waiting for wake-up command...")
    if "hey alexa" or "alexa" or "hello alexa" in wake_sound:
        print("I'm here Nigga!")
        number = random.randint(0, 1)
        if number == 1:
            play_sound()
        else:
            say("Hello there,    how can i be of service")
        query = ""
        try:
            with sr.Microphone() as source:
                listener.adjust_for_ambient_noise(source) 
                print("Listening...")
                voice = listener.listen(source, timeout=6.5)
                print("got it...")
                query = listener.recognize_google(voice)
                query = query.lower()
                print(f'working on...{query}')
                process_alexa(query)
        except Exception as e:
            print(f"Error: {e}")
    
def process_alexa(query):
    # Replace greetings and 'alexa' from the command
    response = query
    if 'play' in response:
        song = response.replace('play', '').strip()
        say('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in response:
        time = datetime.datetime.now().strftime('%I:%M %p')
        say('Current time is ' + time)
    elif 'who is' in response:
        person = response.replace('who is', '').strip()
        info = wikipedia.summary(person, 1)
        print(info)
        say(info)
    elif 'date' in response:
        say('sorry, I have a headache')
    elif 'are you single' in response:
        say('I am in a relationship with wifi')
    elif'send' in response and 'message' in response:
        # Extract the contact name and message from the command
        try:
            # Extract the contact (the word after "send a message to")
            contact = response.replace('send a message to', '').strip().split(' ')[0]  
            say(f'What do you want to tell {contact}?')
            
            # Listen for the message after the prompt
            try:
                with sr.Microphone() as source:
                    listener.adjust_for_ambient_noise(source)
                    print("Listening for the message...")
                    voice = listener.listen(source, timeout=6.5)
                    print("Got it...")
                    message = listener.recognize_google(voice)
                    print(f"Message: {message}")
                    
                    # Prompt for the phone number (including country code) if not already provided
                    phone_number = input(f"Enter {contact}'s phone number (including country code, e.g., +1 for US): ")

                    # Send the message immediately
                    if phone_number and message:
                        say(f'Sending message to {contact}: {message}')
                        pywhatkit.sendwhatmsg_instantly(phone_number, message)  
                    else:
                        say('Sorry, I could not extract the contact or the message.')
            except Exception as e:
                print(f"Error: {e}")
                say('Sorry, I could not hear your message.')
        
        except Exception as e:
            say('Sorry, I could not send the message.')
            print(f"Error: {e}")
    elif 'weather' in response:
        city = response.replace('weather in', '').strip()
        weather_info = get_weather(city)
        say(weather_info)
    
    elif 'remind me to' in response:
        reminder = response.replace('remind me to', '').strip()
        reminders.append(reminder)
        say(f'Reminder added: {reminder}')
    
    elif 'tell me a joke' in response:
        jokes = [
            "Why don’t scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don’t skeletons fight each other? They don’t have the guts."
        ]
        joke = random.choice(jokes)
        say(joke)
    
    elif 'news' in response:
        news_api_key = "96bb1def2547448c88e880166d92014b"  # Replace with your News API key
        url = f"https://newsapi.org/v2/top-headlines?country=ke&apiKey={news_api_key}"
        try:
            response = requests.get(url)
            articles = response.json().get('articles', [])
            if articles:
                say("Here are the latest headlines:")
                for article in articles[:5]:
                    say(article['title'])
            else:
                say("I couldn't find any news right now.")
        except Exception as e:
            print(f"Error: {e}")
            say("There was an error fetching the news.")
    
    elif 'calculate' in response:
        expression = response.replace('calculate', '').strip()
        try:
            result = eval(expression)
            say(f'The result is {result}')
        except Exception as e:
            say("Sorry, I couldn't calculate that.")
    
    
    elif 'define' in response:
        word = response.replace('define', '').strip()
        dictionary_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        try:
            result = requests.get(dictionary_url).json()
            definition = result[0]['meanings'][0]['definitions'][0]['definition']
            say(f"The definition of {word} is: {definition}")
        except Exception as e:
            print(f"Error: {e}")
            say(f"Sorry, I couldn't find a definition for {word}.")
    
    elif 'tell me a story' in response:
        stories = [
            "Once upon a time, in a small village, there was a curious fox...",
            "Long ago, in a dense forest, there lived a wise old owl...",
            "In a faraway kingdom, there was a brave little girl named Ellie..."
        ]
        story = random.choice(stories)
        say(story)

    else:
        say('Please say the command again.')


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


take_command()