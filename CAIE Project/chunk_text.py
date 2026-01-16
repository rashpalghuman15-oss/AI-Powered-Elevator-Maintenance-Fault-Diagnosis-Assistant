import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

print("🔤 Creating search index for elevator manual...")


# Step 1: Read the manual text
with open("Data/manual_text.txt", "r", encoding="utf-8") as f:
    manual_text = f.read()

print(f"Read {len(manual_text)} characters from manual")

# Step 2: Split into chunks (simple method)
chunk_size = 500  # characters per chunk
chunks = []
for i in range(0, len(manual_text), chunk_size):
    chunk = manual_text[i:i+chunk_size]
    if len(chunk.strip()) > 50:  # Only keep meaningful chunks
        chunks.append(chunk.strip())

print(f"Created {len(chunks)} text chunks")

# Step 3: Create embeddings (AI Component 1)
print("Creating embeddings (this may take a minute)...")
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(chunks)

np.save("Data/embeddings.npy", embeddings)
print(f"Saved embeddings to Data/embeddings.npy")

print(f"Created {len(embeddings)} embeddings")

# Step 4: Create search index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype('float32'))

# Step 5: Save everything
# Save index
faiss.write_index(index, "Data/vector_index.faiss")

# Save chunks
with open("Data/chunks.txt", "w", encoding="utf-8") as f:
    for chunk in chunks:
        f.write(chunk + "\n")

print("✅ Index created successfully!")
print(f"   Saved: Data/vector_index.faiss ({index.ntotal} vectors)")
print(f"   Saved: Data/chunks.txt ({len(chunks)} chunks)")

with open("Data/chunks.txt", "w", encoding="utf-8") as f:
    for chunk in chunks:
        f.write(chunk + "\n")
print(f"✅ Saved {len(chunks)} chunks to Data/chunks.txt")

# Quick test
print("\n🧪 Quick test: Searching for 'door fault'...")
query = "door fault"
query_embedding = model.encode([query])
distances, indices = index.search(np.array(query_embedding), 1)
print(f"   Found chunk {indices[0][0]} with distance {distances[0][0]:.3f}")