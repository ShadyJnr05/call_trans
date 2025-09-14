import nltk
from nltk.corpus import stopwords
import string

# Download stopwords once
nltk.download('stopwords')

# Example text (replace with your transcription)
text = "This is an example transcription from the audio file."

# Convert text to lowercase
text = text.lower()

# Remove punctuation
text = text.translate(str.maketrans('', '', string.punctuation))

# Remove stopwords (common words like 'the', 'is', etc.)
stop_words = set(stopwords.words('english'))
words = [word for word in text.split() if word not in stop_words]

# Join cleaned words back into a string
cleaned_text = ' '.join(words)

print("Cleaned Text:", cleaned_text)
