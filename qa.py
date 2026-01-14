import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

print("🤖 Loading Elevator Maintenance Assistant...")

# Load the search model (AI Component 1)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the search index
print("Loading search index...")
index = faiss.read_index("Data/vector_index.faiss")

# Load the chunks
with open("Data/chunks.txt", "r", encoding="utf-8") as f:
    chunks = [line.strip() for line in f]

print(f"✅ System ready! Loaded {len(chunks)} manual sections")

def search_manual(query, top_k=3):
    """
    AI Component 1: Search for relevant manual sections
    """
    # Convert query to embedding
    query_embedding = model.encode([query])
    
    # Search the index
    distances, indices = index.search(np.array(query_embedding), top_k)
    
    # Get the actual chunks
    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(chunks):
            results.append({
                "text": chunks[idx],
                "similarity": float(1 / (1 + distances[0][i])),  # Convert distance to similarity score
                "distance": float(distances[0][i])
            })
    
    return results

def generate_answer(query, search_results):
    """
    AI Component 2: Simple rule-based answer generator (no LLM needed)
    """
    if not search_results:
        return "I couldn't find information about this issue in the manual. Please consult a certified technician."
    
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
    
    # Build answer from search results
    answer_parts = []
    
    # Safety warning (always included)
    answer_parts.append("⚠️ **SAFETY FIRST:** Always turn off power before inspection. Wear safety gear.")
    
    # Add the most relevant manual section
    best_result = search_results[0]
    answer_parts.append(f"**From manual:** {best_result['text'][:300]}...")
    
    # Add diagnostic steps based on issue type
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
    
    return "\n\n".join(answer_parts)

def ask_question(query):
    """
    Main function: Search + Generate answer
    """
    print(f"\n🔍 Searching for: '{query}'")
    
    # Step 1: Search manual (AI Component 1)
    search_results = search_manual(query, top_k=2)
    
    if not search_results:
        return "No relevant information found.", []
    
    print(f"Found {len(search_results)} relevant sections")
    
    # Step 2: Generate answer (AI Component 2)
    answer = generate_answer(query, search_results)
    
    return answer, search_results

# Simple command-line interface
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🛗 ELEVATOR MAINTENANCE ASSISTANT")
    print("="*50)
    print("Type your elevator issue below (or 'quit' to exit)")
    print("Example: 'door not closing properly'")
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
            
            print("\n" + "-"*30)
            print("📖 Sources found in manual:")
            for i, source in enumerate(sources):
                print(f"\nSource {i+1} (relevance: {source['similarity']:.2f}):")
                print(f"{source['text'][:150]}...")