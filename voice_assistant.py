import datetime
import os
import subprocess
import urllib.parse
import webbrowser
import pyttsx3
import speech_recognition as sr


class PersonalVoiceAssistant:
    """Personal Voice Assistant with Speech-to-Text, Rule Mapping, and Text-to-Speech."""

    def __init__(self, assistant_name="Syntecx Voice Assistant"):
        self.assistant_name = assistant_name
        self.recognizer = sr.Recognizer()
        # Adjust pause and energy settings for reliable microphone capture
        self.recognizer.pause_threshold = 0.8
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True

        # Dictionary of sample commands for user reference
        self.sample_commands = {
            "Time & Date": [
                "what is the time",
                "what is today's date",
                "what day is it",
            ],
            "Open Applications": [
                "open notepad",
                "open calculator",
                "open command prompt",
                "open paint",
                "open file explorer",
            ],
            "Web Search & Websites": [
                "search for artificial intelligence",
                "youtube python programming",
                "open google",
                "open github",
                "open linkedin",
                "open wikipedia",
            ],
            "Assistant & System": [
                "hello",
                "who are you",
                "tell me a joke",
                "show sample commands",
                "exit",
            ],
        }

        # Rule-mapping dictionary linking keywords to action methods
        self.command_rules = [
            (["time", "current time"], self.tell_time),
            (["date", "today's date", "what day"], self.tell_date),
            (["open notepad", "launch notepad"], lambda cmd: self.open_app("notepad")),
            (["open calculator", "launch calculator", "calc"], lambda cmd: self.open_app("calc")),
            (["open command prompt", "open cmd", "open terminal"], lambda cmd: self.open_app("cmd")),
            (["open paint", "mspaint"], lambda cmd: self.open_app("mspaint")),
            (["open file explorer", "open explorer"], lambda cmd: self.open_app("explorer")),
            (["open google"], lambda cmd: self.open_website("https://www.google.com", "Google")),
            (["open youtube"], lambda cmd: self.open_website("https://www.youtube.com", "YouTube")),
            (["open github"], lambda cmd: self.open_website("https://github.com", "GitHub")),
            (["open linkedin"], lambda cmd: self.open_website("https://www.linkedin.com", "LinkedIn")),
            (["open wikipedia"], lambda cmd: self.open_website("https://www.wikipedia.org", "Wikipedia")),
            (["youtube "], self.search_youtube),
            (["search for ", "search ", "google "], self.search_web),
            (["sample commands", "help", "what can you do"], lambda cmd: self.show_sample_commands()),
            (["joke", "make me laugh"], self.tell_joke),
            (["who are you", "your name"], self.introduce_self),
            (["hello", "hi ", "hey", "good morning", "good afternoon", "good evening"], self.greet_user),
        ]

    def speak(self, text):
        """Convert text response into audible speech using pyttsx3."""
        print(f"\n[Assistant]: {text}")
        try:
            engine = pyttsx3.init("sapi5")
            voices = engine.getProperty("voices")
            if voices:
                engine.setProperty("voice", voices[0].id)
            engine.setProperty("rate", 175)
            engine.setProperty("volume", 1.0)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"[TTS Warning]: Audio playback unavailable ({e}). Displaying text response only.")

    def listen_command(self):
        """Capture audio from the microphone and convert speech to text."""
        try:
            with sr.Microphone() as source:
                print("\n[Calibrating microphone for background noise... Please wait]")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                print("[Listening... Speak your command now!]")
                audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=8)

            print("[Recognizing speech...]")
            command = self.recognizer.recognize_google(audio, language="en-in")
            print(f"[You said]: \"{command}\"")
            return command.lower().strip()

        except sr.WaitTimeoutError:
            self.speak("Listening timed out because no speech was detected. Please try again.")
            return None
        except sr.UnknownValueError:
            self.speak("Sorry, I could not understand the audio. Please speak clearly.")
            return None
        except sr.RequestError as e:
            self.speak(f"Speech recognition service is unavailable right now. Check your internet connection. ({e})")
            return None
        except OSError:
            self.speak("No working microphone was detected on this system. Switching to text input.")
            fallback = input("Type your command instead: ").strip().lower()
            return fallback if fallback else None
        except Exception as e:
            self.speak(f"An unexpected audio error occurred: {e}")
            return None

    # ==================== ACTION METHODS ====================

    def tell_time(self, _command=""):
        now = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {now}.")

    def tell_date(self, _command=""):
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        self.speak(f"Today is {today}.")

    def open_app(self, app_name):
        app_map = {
            "notepad": ("Notepad", "notepad.exe"),
            "calc": ("Calculator", "calc.exe"),
            "cmd": ("Command Prompt", "cmd.exe"),
            "mspaint": ("Paint", "mspaint.exe"),
            "explorer": ("File Explorer", "explorer.exe"),
        }
        if app_name in app_map:
            label, executable = app_map[app_name]
            try:
                self.speak(f"Opening {label}.")
                subprocess.Popen(executable, shell=True)
            except Exception as e:
                self.speak(f"Failed to open {label}: {e}")

    def open_website(self, url, site_name):
        try:
            self.speak(f"Opening {site_name} in your web browser.")
            webbrowser.open(url)
        except Exception as e:
            self.speak(f"Could not open {site_name}: {e}")

    def search_web(self, command):
        query = command
        for prefix in ["search for ", "search ", "google "]:
            if prefix in query:
                query = query.split(prefix, 1)[1].strip()
                break
        if not query:
            self.speak("What would you like me to search for on Google?")
            return
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={encoded_query}"
        self.speak(f"Searching Google for {query}.")
        webbrowser.open(url)

    def search_youtube(self, command):
        query = command.split("youtube ", 1)[1].strip() if "youtube " in command else ""
        if not query:
            self.speak("What would you like to search on YouTube?")
            return
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://www.youtube.com/results?search_query={encoded_query}"
        self.speak(f"Searching YouTube for {query}.")
        webbrowser.open(url)

    def greet_user(self, _command=""):
        hour = datetime.datetime.now().hour
        if hour < 12:
            greeting = "Good morning"
        elif hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        self.speak(f"{greeting}! How can I help you today?")

    def introduce_self(self, _command=""):
        self.speak(
            f"I am {self.assistant_name}, a Python Personal Voice Assistant built for the Syntecxhub AI Internship."
        )

    def tell_joke(self, _command=""):
        self.speak("Why do Python programmers wear glasses? Because they cannot C!")

    def show_sample_commands(self):
        print("\n" + "=" * 60)
        print("                 SAMPLE VOICE COMMANDS LIST")
        print("=" * 60)
        for category, commands in self.sample_commands.items():
            print(f"\n[{category}]")
            for cmd in commands:
                print(f"  - \"{cmd}\"")
        print("=" * 60)
        self.speak("I have displayed the list of sample commands on your screen.")

    # ==================== RULE DISPATCHER ====================

    def execute_command(self, command):
        """Match spoken or typed text against rule mappings and trigger actions."""
        if not command:
            return True

        # Check for exit commands first
        if command in ["exit", "quit", "stop", "goodbye", "bye"]:
            self.speak("Goodbye! Shutting down the Personal Voice Assistant.")
            return False

        # Exact greeting match for single-word "hi"
        if command == "hi":
            self.greet_user()
            return True

        # Match command against rule list
        for keywords, action in self.command_rules:
            for keyword in keywords:
                if keyword in command:
                    action(command)
                    return True

        # Fallback error handling for unrecognized commands
        self.speak(
            f"Sorry, I did not recognize the command '{command}'. Say 'help' or 'sample commands' to see what I can do."
        )
        return True


def main():
    assistant = PersonalVoiceAssistant()
    assistant.speak("Welcome to the Syntecxhub Personal Voice Assistant.")

    while True:
        print("\n" + "=" * 60)
        print("        SYNTECXHUB - PERSONAL VOICE ASSISTANT")
        print("=" * 60)
        print(" 1. Speak a Single Voice Command (Microphone)")
        print(" 2. Start Continuous Voice Assistant Mode (Microphone Loop)")
        print(" 3. Type a Command (Text Input Mode)")
        print(" 4. View Sample Commands List")
        print(" 5. Exit")
        print("=" * 60)

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            cmd = assistant.listen_command()
            if cmd:
                assistant.execute_command(cmd)

        elif choice == "2":
            assistant.speak(
                "Continuous voice mode activated. Speak your commands, or say 'exit' to return to the menu."
            )
            while True:
                cmd = assistant.listen_command()
                if cmd:
                    keep_running = assistant.execute_command(cmd)
                    if not keep_running:
                        break

        elif choice == "3":
            cmd = input("\nEnter your command (e.g., 'what is the time', 'open notepad'): ").strip().lower()
            if cmd:
                assistant.execute_command(cmd)

        elif choice == "4":
            assistant.show_sample_commands()

        elif choice == "5":
            assistant.speak("Thank you for using the Personal Voice Assistant. Goodbye!")
            break

        else:
            print("\n[Invalid Option]: Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()