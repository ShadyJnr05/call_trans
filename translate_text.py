from deep_translator import GoogleTranslator

# Ask user for target language
target_lang = input("Enter target language code (e.g., 'fr' for French, 'es' for Spanish, 'de' for German): ")

# Read the text from the transcription file
with open("transcription.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Translate the text
translated_text = GoogleTranslator(source='auto', target=target_lang).translate(text)

print("\nOriginal Text:")
print(text)
print(f"\nTranslated Text ({target_lang}):")
print(translated_text)

# Save translation
with open("translation.txt", "w", encoding="utf-8") as f:
    f.write(translated_text)

print("✅ Translation saved to translation.txt")


