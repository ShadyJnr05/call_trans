import sqlite3

# Connect to database
conn = sqlite3.connect("transcripts.db")
c = conn.cursor()

# Ask user for search keyword
keyword = input("Enter a keyword to search in transcriptions or translations: ")

# Search in transcription or translation
c.execute('''SELECT id, audio_file, transcription, translation, language
             FROM transcripts
             WHERE transcription LIKE ? OR translation LIKE ?''', 
          (f'%{keyword}%', f'%{keyword}%'))

results = c.fetchall()

if results:
    print(f"\n✅ Found {len(results)} result(s):\n")
    for row in results:
        print(f"ID: {row[0]}")
        print(f"Audio File: {row[1]}")
        print(f"Transcription: {row[2]}")
        print(f"Translation ({row[4]}): {row[3]}")
        print("-" * 40)
else:
    print("❌ No results found for that keyword.")

conn.close()
