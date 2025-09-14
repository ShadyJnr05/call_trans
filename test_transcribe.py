import speech_recognition as sr
import re

recognizer = sr.Recognizer()

# Read the audio file
with sr.AudioFile("audio.wav") as source:
    audio = recognizer.record(source)

# Convert speech to text
text = recognizer.recognize_google(audio)

# Clean the text: remove numbers and extra spaces
clean_text = re.sub(r'\d+', '', text)  # remove digits
clean_text = re.sub(r'\s+', ' ', clean_text).strip()  # normalize spaces

print("Cleaned Text:")
print(clean_text)

# Save to file
with open("transcription.txt", "w", encoding="utf-8") as f:
    f.write(clean_text)

print("✅ Transcription saved to transcription.txt")
