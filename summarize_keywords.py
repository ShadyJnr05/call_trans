from transformers import pipeline

# Example cleaned text (replace with your cleaned_text variable)
text = "your cleaned transcription text goes here"

# Load summarization pipeline
summarizer = pipeline("summarization")

# Summarize the text
summary = summarizer(text, max_length=50, min_length=20, do_sample=False)
print("Summary:", summary[0]['summary_text'])

# Keyword extraction using a simple method
words = text.split()
# Count frequency of each word
freq = {}
for word in words:
    freq[word] = freq.get(word, 0) + 1

# Get top 5 keywords
keywords = sorted(freq, key=freq.get, reverse=True)[:5]
print("Keywords:", keywords)
