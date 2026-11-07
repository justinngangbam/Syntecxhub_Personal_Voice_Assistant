# Personal Voice Assistant

A Python-based **Personal Voice Assistant** built using `SpeechRecognition` and `pyttsx3` as part of the Artificial Intelligence Internship at **Syntecxhub**.

## Features

- **Speech-to-Text Input:** Captures spoken commands through the microphone with ambient noise calibration and transcribes audio using Google Speech Recognition (`SpeechRecognition`).
- **Rule-Based Command Mapping:** Maps spoken and typed commands to system actions including telling the current time and date, opening desktop applications (Notepad, Calculator, Command Prompt, Paint, File Explorer), and searching Google or YouTube.
- **Text-to-Speech Response:** Converts assistant replies into offline spoken audio using `pyttsx3` (Windows SAPI5 engine).
- **Sample Commands List:** Displays a categorized list of supported voice commands directly in the terminal.
- **Robust Error Handling:** Gracefully handles microphone timeouts, unrecognized speech, network issues, and missing audio hardware with a text-input fallback mode.

## Tech Stack

- **Language:** Python 3.13
- **Libraries:**
  - `SpeechRecognition` — Speech-to-text transcription
  - `pyttsx3` — Offline text-to-speech synthesis
  - `PyAudio` — Microphone audio stream capture

## Project Structure

```text
Syntecxhub_Personal_Voice_Assistant/
├── voice_assistant.py   # Main Personal Voice Assistant application
├── requirements.txt     # Required Python dependencies
└── README.md            # Project documentation
