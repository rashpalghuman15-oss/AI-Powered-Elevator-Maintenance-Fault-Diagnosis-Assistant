input_file = "data/clean_faults.txt"

with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

chunk_size = 500
chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

print(f"Total chunks created: {len(chunks)}")
print("Sample chunk:\n")
print(chunks[0])