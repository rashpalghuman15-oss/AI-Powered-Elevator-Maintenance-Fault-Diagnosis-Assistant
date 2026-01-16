from pypdf import PdfReader

print("📄 Extracting text from PDF...")


# Read PDF
pdf_reader = PdfReader("Data/Faults_Recommended_Actions.pdf")

# Extract text from all pages
all_text = ""
for page in pdf_reader.pages:
    text = page.extract_text()
    if text:
        all_text += text + "\n"

# Save to file
with open("Data/manual_text.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print(f"✅ Done! Saved {len(all_text)} characters to Data/manual_text.txt")
print(f"   Processed {len(pdf_reader.pages)} pages")