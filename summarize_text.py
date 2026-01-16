from transformers import pipeline

from clean_text import cleaned_text  # your cleaned PDF text

# Initialize summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)  # device=-1 uses CPU

# Summarize in chunks (to avoid token limits)
max_chunk = 1000  # characters per chunk
text_chunks = [cleaned_text[i:i+max_chunk] for i in range(0, len(cleaned_text), max_chunk)]

summary = ""
for chunk in text_chunks:
    if len(chunk.strip()) > 0:  # Skip empty chunks
        s = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
        summary += s[0]['summary_text'] + " "

# Optional: print summary
if __name__ == "__main__":
    print("Summary:\n", summary.strip())