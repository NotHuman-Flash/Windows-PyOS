import os
import speech_recognition as sr
import pyttsx3
from openai import OpenAI

# 🔑 OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🎤 + 🔊 setup
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You:", command)
        return command
    except:
        speak("Sorry, I didn't catch that.")
        return ""

# 🤖 AI
def ask_ai(prompt):
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        return response.output_text.strip()
    except Exception as e:
        return f"Error: {e}"

# 🔊 Volume control
def change_volume(action):
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    if action == "up":
        volume.SetMasterVolumeLevelScalar(min(volume.GetMasterVolumeLevelScalar() + 0.1, 1.0), None)
        return "Volume increased"

    elif action == "down":
        volume.SetMasterVolumeLevelScalar(max(volume.GetMasterVolumeLevelScalar() - 0.1, 0.0), None)
        return "Volume decreased"

    elif action == "mute":
        volume.SetMute(1, None)
        return "Muted"

# ⚙️ Commands
def handle_command(command):
    if "volume up" in command:
        return change_volume("up")

    elif "volume down" in command:
        return change_volume("down")

    elif "mute" in command:
        return change_volume("mute")

    elif "open notepad" in command:
        os.system("notepad")
        return "Opening Notepad"

    elif "open settings" in command:
        os.system("start ms-settings:")
        return "Opening Settings"

    elif "exit" in command or "stop" in command:
        return "exit"

    elif command:
        return ask_ai(command)

    return ""

# 🔁 Main loop (always listening)
def run_assistant():
    speak("Assistant started. Listening for commands.")

    while True:
        command = listen()

        if not command:
            continue

        response = handle_command(command)

        if response == "exit":
            speak("Goodbye!")
            break

        speak(response)

if __name__ == "__main__":
    run_assistant()