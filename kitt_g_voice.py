import warnings
import pyaudio
import wave
import whisper
import openai
import keyboard
import os
import tkinter as tk
from tkinter import simpledialog
from google.cloud import texttospeech
from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play

# Initialize Google Cloud Text-to-Speech client
client = texttospeech.TextToSpeechClient()

# Define ANSI escape sequences for text color
colors = {
    "blue": "\033[94m",
    "orange": "\033[93m",
    "yellow": "\033[93m",
    "white": "\033[97m",
    "red": "\033[91m",
    "magenta": "\033[35m",
    "green": "\033[32m",
    "reset": "\033[0m"
}

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

openai.api_base = "http://localhost:1234/v1"
openai.api_key = "not-needed"

whisper_model = whisper.load_model("tiny")  # orig=base

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000  # orig = 16000
CHUNK = 1024
audio = pyaudio.PyAudio()

def speak(text, sample_rate_hertz=16000):
    # Set up the text request
    synthesis_input = texttospeech.SynthesisInput(text=text)
    # Configure the voice parameters
    voice = texttospeech.VoiceSelectionParams(
       language_code="en-GB",
       name="en-GB-Neural2-A",
       ssml_gender=texttospeech.SsmlVoiceGender.FEMALE  # Or MALE 
   )
    # Configure the audio output format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        sample_rate_hertz=sample_rate_hertz
    )
    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    # Save the output to an MP3 file and play it
    with open("temp_output.mp3", "wb") as out:
        out.write(response.audio_content)
    audio = AudioSegment.from_mp3("temp_output.mp3")
    play(audio)  # Play the audio directly

def read_file_content(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print("File not found.")
        return None

# Initial greeting
system_message = read_file_content("system_message.txt")
if system_message is None:
    exit()  # Exit if system message file not found

initial_message = "Welcome to a new episode of Videotronic Maker, This is KITT, his personal A.I. assistant. I exist in the home PC of Videotronic Maker and I am locally run via LM Studio. LM Studio is a software company located in Brooklyn, New York, so it's fair to say that Brooklyn is in the house! Learn with Videotronic Maker as he learns!"
speak(initial_message, sample_rate_hertz=16000)

def record_audio():
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print(f"{colors['green']}Start speaking... (Press 'N' to stop){colors['reset']}")
    frames = []

    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        if keyboard.is_pressed('n'):
            print(f"{colors['red']}Stopping recording.{colors['reset']}")
            break

    stream.stop_stream()
    stream.close()

    wf = wave.open("temp_audio.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return "temp_audio.wav"

def get_user_input():
    """Create a GUI dialog for user input."""
    ROOT = tk.Tk()
    ROOT.withdraw()  # Hide the main Tkinter window
    user_input = simpledialog.askstring(title="Text Input", prompt="Type your input:")
    return user_input

def process_input(input_text):
    conversation = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": input_text}
    ]

    max_response_tokens = 150  # Control KITT's response length

    if input_text.lower() in ['exit', 'bye', 'end']:
        farewell_response = "Goodbye sir!"
        print(f"{colors['magenta']}KITT:{colors['reset']} {farewell_response}")
        speak(farewell_response)
        exit()  # Exiting the script gracefully

    completion = openai.ChatCompletion.create(
        model="local-model",
        messages=conversation,
        temperature=0.7,
        top_p=0.9,  
        top_k=40    
    )

    assistant_reply = completion.choices[0].message.content
    print(f"{colors['magenta']}KITT:{colors['reset']} {assistant_reply}")
    speak(assistant_reply)


    # Check for exit condition
    if input_text.lower() in ['exit', 'bye', 'end']:
        print("Exiting the conversation.")
        exit()  # Exiting the script gracefully

print(f"{colors['yellow']}Ready to record. (Press 'B' to start, 'M' to type){colors['reset']}")

while True:
    try:
        if keyboard.is_pressed('b'):  # Start recording when 'B' is pressed
            audio_file = record_audio()
            transcribe_result = whisper_model.transcribe(audio_file)
            transcribed_text = transcribe_result["text"]
            print(f"{colors['blue']}VTM:{colors['reset']} {transcribed_text}")
            process_input(transcribed_text)
            os.remove(audio_file)  # Cleanup

        elif keyboard.is_pressed('m'):  # Use the GUI for input when 'M' is pressed
            typed_input = get_user_input()
            if typed_input:  # Ensure input is not None or empty
                print(f"{colors['blue']}VTM typed:{colors['reset']} {typed_input}")  # Print the typed input in the terminal
                process_input(typed_input)

    except KeyboardInterrupt:
        print("\nExiting...")
        break  # Correctly placed to exit the loop upon a KeyboardInterrupt

audio.terminate()
