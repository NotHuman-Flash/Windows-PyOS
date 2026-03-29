import pyttsx3
from pathlib import Path

script_dir = Path(__file__).resolve().parent
word_bank_path = script_dir / "demo-word_bank.txt"

if not word_bank_path.exists():
    alternate_path = script_dir / "demo" / "demo-word_bank.txt"
    if alternate_path.exists():
        word_bank_path = alternate_path
    else:
        raise FileNotFoundError(
            f"word bank not found. checked: {word_bank_path} and {alternate_path}"
        )

with word_bank_path.open("r", encoding="utf-8") as word_file:
    text = word_file.read()

engine = pyttsx3.init()
engine.say(text)
engine.runAndWait()