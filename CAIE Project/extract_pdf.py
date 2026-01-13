from pypdf import PdfReader

# Load the PDF
reader = PdfReader("data/Faults_Recommended_Actions.pdf")

# Store all extracted text
all_text = ""

# Loop through pages
for page in reader.pages:
    all_text += page.extract_text() + "\n"

# Save extracted text to file
with open("data/Faults_Recommended_Actions.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print("Text extraction complete!")