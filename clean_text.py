import re

from extract_pdf import extract_pdf_text  # import the function

# ---------------------------
# Step 1: Get extracted text
# ---------------------------
extracted_text = extract_pdf_text()  # call the function to get text

# ---------------------------
# Step 2: Clean text function
# ---------------------------
def clean_text(text):
    """Clean text by removing extra whitespace and special characters."""
    # Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters, keep alphanumeric and basic punctuation
    text = re.sub(r'[^A-Za-z0-9.,:;!?() ]+', '', text)
    return text.strip()

# ---------------------------
# Step 3: Create variable for import
# ---------------------------
cleaned_text = clean_text(extracted_text)  # ready to import in other scripts

# ---------------------------
# Optional test
# ---------------------------
if __name__ == "__main__":
    print(cleaned_text[:500])  # first 500 characters