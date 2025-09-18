import speech_recognition as sr
import re
from deep_translator import GoogleTranslator
from pydub import AudioSegment
import os
import sqlite3

# Step 1: Ask user for audio file
audio_file = input("Enter audio file name (e.g., audio.wav or audio.mp3): ")

# Step 2: Convert to WAV if needed
file_name, file_ext = os.path.splitext(audio_file)
if file_ext.lower() != ".wav":
    try:
        print(f"Converting {audio_file} to WAV...")
        audio = AudioSegment.from_file(audio_file)
        audio_file = f"{file_name}.wav"
        audio.export(audio_file, format="wav")
        print(f"Conversion complete: {audio_file}")
    except Exception as e:
        print(f"❌ Failed to convert audio: {e}")
        exit()

# Step 3: Initialize recognizer
# Step 3: Initialize recognizer
recognizer = sr.Recognizer()

try:
    # Step 4: Read and transcribe audio
    with sr.AudioFile(audio_file) as source:
        print("Listening to audio...")
        audio = recognizer.record(source)
    
    print("Transcribing...")
    text = recognizer.recognize_google(audio)

    # Step 5: Clean text
    clean_text = re.sub(r'\d+', '', text)  # remove digits
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()  # normalize spaces

    # Step 6: Save transcription
    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write(clean_text)

    print("\n✅ Transcription completed:")
    print(clean_text)

    # Step 7: Ask user for translation language
    target_lang = input("\nEnter target language code (e.g., 'fr' for French, 'es' for Spanish): ")

    # Step 8: Translate
    translated_text = GoogleTranslator(source='auto', target=target_lang).translate(clean_text)

    # Step 9: Save translation
    with open("translation.txt", "w", encoding="utf-8") as f:
        f.write(translated_text)

    print(f"\n✅ Translation ({target_lang}) completed:")
    print(translated_text)

    # Step 10: Save all info to database
    conn = sqlite3.connect("transcripts.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS transcripts
                 (id INTEGER PRIMARY KEY,
                  audio_file TEXT,
                  transcription TEXT,
                  translation TEXT,
                  language TEXT)''')

    c.execute('''INSERT INTO transcripts (audio_file, transcription, translation, language)
                 VALUES (?, ?, ?, ?)''',
              (audio_file, clean_text, translated_text, target_lang))

    conn.commit()
    conn.close()

    print("\n✅ Data saved to transcripts.db")

except FileNotFoundError:
    print("❌ Error: Audio file not found. Make sure it's in the same folder.")
except Exception as e:
    print(f"❌ An error occurred: {e}")
