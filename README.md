# Alexa by Vick

## Project Overview

This project is a voice-activated assistant built using Python. It allows users to sign up, log in, and interact with the assistant through voice commands. The assistant performs various tasks such as playing music, telling jokes, providing weather updates, setting reminders, and more. It uses text-to-speech (TTS) for responses and speech recognition for voice input.

### Key Features:
- **User Authentication**: Users can sign up and log in with their credentials stored in a SQLite database.
- **Voice Commands**: The assistant listens to user voice commands and responds accordingly.
- **TTS and Notifications**: The assistant uses `gTTS` (Google Text-to-Speech) for speech output and plays notification sounds using Pygame.
- **Weather and News**: Fetches real-time weather data using OpenWeather API and the latest news using the NewsAPI.
- **Music and YouTube Integration**: Uses `pywhatkit` to play songs on YouTube based on voice commands.
- **Jokes and Trivia**: The assistant can tell jokes and provide interesting trivia facts.

## Requirements

To run this project, you need to have Python 3.x installed, along with the following dependencies:

- `pygame`
- `pywhatkit`
- `requests`
- `wikipedia`
- `gTTS`
- `werkzeug`
- `SpeechRecognition`
- `sqlite3`

### Install dependencies

You can install the required dependencies using pip:

```bash
pip install pygame pywhatkit requests wikipedia gtts werkzeug SpeechRecognition
```

alexa/
│
├── app.py                  # Main program file to run the assistant
├── database/               # Folder containing database files
│   └── user_data.db        # SQLite database for storing user information
├── models.py               # This is where all the actions of ORM happends
├── create_tables.py        # this file is excecuted once during the installation to create tables
├── delete_tables.py        # this file is excecuted to delete all records in the tables
├── actions.py              # This is where all the actions of database comminication take place
├── wake.mp3                # Wake-up sound file
└── README.md               # List of project dependencies

## Usage
Sign Up: When you run the program for the first time, you can choose to sign up by providing a username, password, and name. This will create a user entry in the database.

Login: If you have already signed up, you can log in by providing your credentials.

Voice Commands: After logging in, you can interact with the assistant by saying commands like:

"Hey Alexa, play a song"
"What’s the weather in [city]?"
"Tell me a joke"
"What’s the time?"
"Send a message to [contact]"
"Set a reminder"
And more!
Example Interaction
1. Signup
2. Login
Choose an option (1 or 2): 2
Enter your username: alexa
Enter your password: ********
Welcome back, Alexa!
You are now authenticated. Enjoy the app!

Listening for wake-up command...
I'm here!
Listening for a command...
Got it... Playing Shape of You by Ed Sheeran

## Notes
The program uses gTTS to convert text to speech. Ensure that your system has access to an internet connection for this functionality.
The program also uses pywhatkit to play music on YouTube. Ensure your system can open web pages to use this feature.
You will need API keys for NewsAPI and OpenWeather to fetch news and weather data. Make sure to replace the placeholder API keys in the code with your own keys.
Contributing
If you would like to contribute to this project, feel free to fork the repository and submit pull requests. For any issues or feature requests, please open an issue on the GitHub repository.

## License
This project is licensed under the MIT License.



This README provides a clear overview of your project, its features, how to install dependencies, and instructions for usage. You can customize the information based on your exact project details.
