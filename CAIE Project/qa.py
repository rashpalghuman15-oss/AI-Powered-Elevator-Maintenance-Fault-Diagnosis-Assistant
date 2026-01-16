import numpy as np
import os
import re

# qa.py - AI Elevator Maintenance Assistant (No sentence-transformers version)
print("🤖 Loading Elevator Maintenance Assistant...")

def load_data():
    """Load chunks and create simple embeddings"""
    try:
        # Load chunks
        with open("Data/chunks.txt", "r", encoding="utf-8") as f:
            chunks = [line.strip() for line in f if line.strip()]
        
        # Create simple TF-IDF like embeddings
        if chunks:
            # Create vocabulary from chunks
            vocabulary = {}
            chunk_vectors = []
            
            for chunk in chunks:
                words = re.findall(r'\b\w+\b', chunk.lower())
                word_count = {}
                for word in words:
                    if len(word) > 2:  # Ignore short words
                        if word not in vocabulary:
                            vocabulary[word] = len(vocabulary)
                        word_id = vocabulary[word]
                        word_count[word_id] = word_count.get(word_id, 0) + 1
                
                # Create vector for this chunk
                vector = np.zeros(len(vocabulary))
                for word_id, count in word_count.items():
                    vector[word_id] = count
                chunk_vectors.append(vector)
            
            embeddings = np.array(chunk_vectors)
            print(f"✅ Loaded {len(chunks)} chunks with {len(vocabulary)} unique words")
            return chunks, embeddings, vocabulary
        else:
            return [], None, None
            
    except FileNotFoundError:
        print("⚠️ Data files not found. Using fallback mode.")
        return [], None, None

chunks, embeddings, vocabulary = load_data()

def create_query_vector(query, vocabulary):
    """Convert query to vector using same vocabulary"""
    if vocabulary is None:
        return None
    
    words = re.findall(r'\b\w+\b', query.lower())
    vector = np.zeros(len(vocabulary))
    
    for word in words:
        if len(word) > 2 and word in vocabulary:
            word_id = vocabulary[word]
            vector[word_id] += 1
    
    return vector

def search_manual_simple(query, top_k=3):
    """Simple similarity search"""
    if embeddings is None or len(chunks) == 0 or vocabulary is None:
        return []
    
    # Convert query to vector
    query_vector = create_query_vector(query, vocabulary)
    if query_vector is None or np.sum(query_vector) == 0:
        return []
    
    # Simple cosine similarity
    # Normalize vectors
    chunk_norms = np.linalg.norm(embeddings, axis=1)
    query_norm = np.linalg.norm(query_vector)
    
    if query_norm == 0:
        return []
    
    # Avoid division by zero
    chunk_norms = np.where(chunk_norms == 0, 1, chunk_norms)
    
    # Calculate similarities
    similarities = np.dot(embeddings, query_vector) / (chunk_norms * query_norm)
    
    # Get top k indices
    if len(similarities) > top_k:
        top_indices = np.argpartition(similarities, -top_k)[-top_k:]
        top_indices = top_indices[np.argsort(-similarities[top_indices])]
    else:
        top_indices = np.argsort(-similarities)
    
    # Get results
    results = []
    for idx in top_indices:
        if idx < len(chunks) and similarities[idx] > 0.1:  # Threshold
            results.append({
                "text": chunks[idx],
                "similarity": float(similarities[idx])
            })
    
    return results

def generate_answer(query, search_results):
    """AI Component 2: Rule-based answer generator"""
    if not search_results:
        return "I couldn't find information about this issue in the manual. Please consult a certified technician.", []
    
    # Extract keywords from query
    query_lower = query.lower()
    
    # Check for common issues
    if any(word in query_lower for word in ["door", "gate", "entrance"]):
        issue_type = "door issue"
    elif any(word in query_lower for word in ["noise", "sound", "loud"]):
        issue_type = "noise issue"
    elif any(word in query_lower for word in ["stop", "stuck", "not moving"]):
        issue_type = "movement issue"
    elif any(word in query_lower for word in ["error", "code", "fault"]):
        issue_type = "error code"
    else:
        issue_type = "general issue"
    
    # Build answer
    answer_parts = []
    
    # Safety warning (always first)
    answer_parts.append("⚠️ **SAFETY FIRST:** Always turn off power before inspection. Wear safety gear.")
    
    # Add the most relevant manual section
    best_result = search_results[0]
    answer_parts.append(f"**From manual:** {best_result['text'][:300]}...")
    
    # Add diagnostic steps
    answer_parts.append(f"\n**For {issue_type}, follow these steps:**")
    
    steps = {
        "door issue": [
            "1. Check door sensors for obstructions",
            "2. Inspect door tracks for debris",
            "3. Verify door closing force settings",
            "4. Test safety edges"
        ],
        "noise issue": [
            "1. Identify noise location (motor, cables, guides)",
            "2. Check lubrication levels",
            "3. Inspect roller guides",
            "4. Tighten loose components"
        ],
        "movement issue": [
            "1. Check power supply",
            "2. Verify control system signals",
            "3. Inspect safety circuits",
            "4. Check brake operation"
        ],
        "error code": [
            "1. Note the exact error code",
            "2. Check manual error code list",
            "3. Reset system if safe",
            "4. Document before/after status"
        ]
    }
    
    answer_parts.extend(steps.get(issue_type, [
        "1. Review the manual section above",
        "2. Perform visual inspection",
        "3. Check all safety devices",
        "4. Contact supervisor if unsure"
    ]))
    
    # When to call for help
    answer_parts.append("\n**Call certified technician if:**")
    answer_parts.append("- Problem persists after basic checks")
    answer_parts.append("- Safety circuit is faulting")
    answer_parts.append("- Electrical components are damaged")
    
    return "\n\n".join(answer_parts), search_results

def ask_question(query):
    """Main function: Search + Generate answer"""
    print(f"\n🔍 Searching for: '{query}'")
    
    # Step 1: Search manual (AI Component 1)
    search_results = search_manual_simple(query, top_k=2)
    
    if not search_results:
        # Fallback response
        fallback_response = """⚠️ **SAFETY FIRST:** Always turn off power and wear protective gear.
        
        **General Maintenance Steps:**
        1. Perform visual inspection of the affected area
        2. Check all safety switches and circuits
        3. Consult the physical maintenance manual
        4. Contact a certified technician if unsure
        
        **Note:** AI semantic search is analyzing the manual..."""
        return fallback_response, []
    
    print(f"Found {len(search_results)} relevant sections (similarity: {search_results[0]['similarity']:.2f})")
    
    # Step 2: Generate answer (AI Component 2)
    answer, sources = generate_answer(query, search_results)
    
    return answer, sources

# For local testing
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🛗 ELEVATOR MAINTENANCE ASSISTANT")
    print("="*50)
    
    while True:
        query = input("\nYour issue: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if query:
            answer, sources = ask_question(query)
            
            print("\n" + "="*50)
            print("💡 MAINTENANCE ADVICE:")
            print("="*50)
            print(answer)