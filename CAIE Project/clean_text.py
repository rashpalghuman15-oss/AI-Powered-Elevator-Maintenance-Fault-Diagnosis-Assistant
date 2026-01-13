import re

input_file = "data/Faults_Recommended_Actions.txt"
output_file = "data/clean_faults.txt"

with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# Basic cleaning
text = re.sub(r"\s+", " ", text)  # Collapse multiple whitespaces
text = text.replace("\x00", "")   # Remove null characters
text = text.strip()               # Remove leading/trailing whitespace

with open(output_file, "w", encoding="utf-8") as f:
    f.write(text)

print("Text cleaned and saved!")