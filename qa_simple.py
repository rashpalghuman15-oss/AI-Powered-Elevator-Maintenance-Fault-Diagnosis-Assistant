import numpy as np
import os
import re

# qa_simple.py - Simple Elevator Maintenance Assistant
print("🤖 Loading Elevator Maintenance Assistant...")


def load_chunks():
    """Load text chunks from file"""
    try:
        with open("Data/chunks.txt", "r", encoding="utf-8") as f:
            chunks = [line.strip() for line in f if line.strip()]
        return chunks
    except:
        return []

def simple_search(query, chunks, top_k=3):
    """Simple keyword-based search (AI Component 1)"""
    if not chunks:
        return []
    
    query_words = set(word.lower() for word in re.findall(r'\b\w+\b', query) if len(word) > 3)
    
    if not query_words:
        return []
    
    results = []
    for i, chunk in enumerate(chunks):
        chunk_lower = chunk.lower()
        # Count matching words
        matches = sum(1 for word in query_words if word in chunk_lower)
        if matches > 0:
            similarity = matches / len(query_words)
            results.append({
                "text": chunk,
                "similarity": similarity,
                "index": i
            })
    
    # Sort by similarity
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]

def generate_advice(query, search_results):
    """AI Component 2: Rule-based advice generator"""
    if not search_results:
        return """⚠️ **SAFETY FIRST:** Always turn off power before inspection. Wear safety gear.
        
        **General Maintenance Steps:**
        1. Perform visual inspection of the affected area
        2. Check all safety switches and circuits
        3. Consult the physical maintenance manual
        4. Contact a certified technician if unsure""", []
    
    # Analyze query
    query_lower = query.lower()
    
    # Determine issue type
    if any(word in query_lower for word in ["door", "gate", "entrance"]):
        issue_type = "door issue"
        steps = [
            "1. Check door sensors for obstructions",
            "2. Inspect door tracks for debris",
            "3. Verify door closing force settings",
            "4. Test safety edges"
        ]
    elif any(word in query_lower for word in ["noise", "sound", "loud", "grinding"]):
        issue_type = "noise issue"
        steps = [
            "1. Identify noise location (motor, cables, guides)",
            "2. Check lubrication levels",
            "3. Inspect roller guides",
            "4. Tighten loose components"
        ]
    elif any(word in query_lower for word in ["stop", "stuck", "not moving", "stationary"]):
        issue_type = "movement issue"
        steps = [
            "1. Check power supply",
            "2. Verify control system signals",
            "3. Inspect safety circuits",
            "4. Check brake operation"
        ]
    elif any(word in query_lower for word in ["error", "code", "fault", "e5", "e6"]):
        issue_type = "error code"
        steps = [
            "1. Note the exact error code",
            "2. Check manual error code list",
            "3. Reset system if safe",
            "4. Document before/after status"
        ]
    else:
        issue_type = "general issue"
        steps = [
            "1. Review the manual section above",
            "2. Perform visual inspection",
            "3. Check all safety devices",
            "4. Contact supervisor if unsure"
        ]
    
    # Build response
    response_parts = []
    response_parts.append("⚠️ **SAFETY FIRST:** Always turn off power before inspection. Wear safety gear.")
    
    if search_results:
        best_chunk = search_results[0]['text'][:300]
        response_parts.append(f"**From manual:** {best_chunk}...")
    
    response_parts.append(f"\n**For {issue_type}, follow these steps:**")
    response_parts.extend(steps)
    
    response_parts.append("\n**Call certified technician if:**")
    response_parts.append("- Problem persists after basic checks")
    response_parts.append("- Safety circuit is faulting")
    response_parts.append("- Electrical components are damaged")
    
    return "\n\n".join(response_parts), search_results

def ask_question(query):
    """Main function combining both AI components"""
    # Load data
    chunks = load_chunks()
    
    # AI Component 1: Search
    search_results = simple_search(query, chunks, top_k=2)
    
    # AI Component 2: Generate advice
    advice, sources = generate_advice(query, search_results)
    
    return advice, sources

# For testing
if __name__ == "__main__":
    print("🛗 ELEVATOR MAINTENANCE ASSISTANT")
    print("="*50)
    
    test_queries = [
        "door not closing properly",
        "error code E5 showing",
        "grinding noise from elevator",
        "elevator stuck between floors"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing: '{query}'")
        advice, sources = ask_question(query)
        print(f"📋 Advice ({len(advice)} chars):")
        print(advice[:200] + "...")
        print(f"📖 Sources found: {len(sources)}")