# Import necessary libraries
import warnings          # Import warnings module to suppress warnings
import pyaudio           # Import pyaudio library for audio I/O
import wave              # Import wave module to read and write WAV files
import whisper           # Import whisper library for audio transcription
import openai            # Import openai library for AI-based conversation
import keyboard          # Import keyboard library for detecting key presses
import os                # Import os module for system operations
import tkinter as tk     # Import tkinter library for GUI dialogs
from tkinter import simpledialog  # Import simpledialog from tkinter for user input dialog
from google.cloud import texttospeech  # Import texttospeech module from google.cloud
from playsound import playsound        # Import playsound function for playing audio files
from pydub import AudioSegment         # Import AudioSegment class from pydub
from pydub.playback import play       # Import play function from pydub for audio playback

# Initialize Google Cloud Text-to-Speech client
client = texttospeech.TextToSpeechClient()

# Define ANSI escape sequences for text color
colors = {
    "blue": "\033[94m",     # Blue color for VTM messages
    "orange": "\033[93m",   # Orange color (unused)
    "yellow": "\033[93m",   # Yellow color for ready message
    "white": "\033[97m",    # White color (unused)
    "red": "\033[91m",      # Red color for stopping recording message
    "magenta": "\033[35m",  # Magenta color for KITT messages
    "green": "\033[32m",    # Green color for start recording message
    "reset": "\033[0m"      # Reset color
}

# Filter out FP16 warning messages
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

# Set up OpenAI API
openai.api_base = "http://localhost:1234/v1"  # Set the API base URL
openai.api_key = "not-needed"                  # Set the API key (not needed for local model)

# Load whisper model for audio transcription
whisper_model = whisper.load_model("tiny")  # Load the whisper model

# Define audio parameters
FORMAT = pyaudio.paInt16  # Set audio format to 16-bit PCM
CHANNELS = 1               # Set number of channels to mono
RATE = 8000                # Set sample rate to 8000 Hz (originally 16000 Hz)
CHUNK = 1024               # Set chunk size for audio I/O

# Initialize PyAudio instance
audio = pyaudio.PyAudio()

# Define a function to synthesize and speak text
def speak(text, sample_rate_hertz=16000):
    # Set up the text request
    synthesis_input = texttospeech.SynthesisInput(text=text)
    # Configure the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-GB",
        name="en-GB-Neural2-A",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
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
    play(audio)

# Define a function to read content from a file
def read_file_content(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print("File not found.")
        return None

# Initial greeting message
system_message = read_file_content("system_message.txt")
if system_message is None:
    exit()  # Exit if system message file not found

# Define the initial greeting message
initial_message = "Welcome to a new episode of Videotronic Maker, This is KITT, his personal A.I. assistant. I exist in the home PC of Videotronic Maker and I am locally run via LM Studio. LM Studio is a software company located in Brooklyn, New York, so it's fair to say that Brooklyn is in the house! Learn with Videotronic Maker as he learns!"
speak(initial_message, sample_rate_hertz=16000)  # Speak the initial greeting message

# Define a function to record audio
def record_audio():


    # Open the audio stream for recording
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

    # Write the recorded audio to a WAV file
    wf = wave.open("temp_audio.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return "temp_audio.wav"

# Define a function to get user input via GUI dialog
def get_user_input():
    ROOT = tk.Tk()
    ROOT.withdraw()
    user_input = simpledialog.askstring(title="Text Input", prompt="Type your input:")
    return user_input

# Define a function to process user input
def process_input(input_text):
    # Construct conversation messages
    conversation = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": input_text}
    ]

    # Set max response tokens for AI conversation
    max_response_tokens = 150

    # Check for exit conditions
    if input_text.lower() in ['exit', 'bye', 'end']:
        farewell_response = "Goodbye sir!"
        print(f"{colors['magenta']}KITT:{colors['reset']} {farewell_response}")
        speak(farewell_response)
        exit()

    # Generate AI-based response
    completion = openai.ChatCompletion.create(
        model="local-model",
        messages=conversation,
        temperature=0.7,
        top_p=0.9,
        top_k=40
    )

    # Get assistant's reply from AI completion
    assistant_reply = completion.choices[0].message.content
    print(f"{colors['magenta']}KITT:{colors['reset']} {assistant_reply}")
    speak(assistant_reply)

    # Check for exit conditions again
    if input_text.lower() in ['exit', 'bye', 'end']:
        print("Exiting the conversation.")
        exit()

# Main loop for recording and processing audio/text input
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
        break  # Exit the loop upon a KeyboardInterrupt

# Terminate PyAudio instance
audio.terminate()
