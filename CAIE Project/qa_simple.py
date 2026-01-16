import numpy as np
import os
import re

# qa_simple.py - Simple version without complex dependencies
print("🤖 Loading Elevator Maintenance Assistant...")


def simple_search(query, chunks):
    """Simple keyword-based search"""
    if not chunks:
        return []
    
    query_words = set(query.lower().split())
    results = []
    
    for i, chunk in enumerate(chunks):
        chunk_lower = chunk.lower()
        matches = sum(1 for word in query_words if word in chunk_lower and len(word) > 3)
        if matches > 0:
            results.append({
                "text": chunk,
                "similarity": matches / len(query_words)
            })
    
    # Sort by similarity
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:3]

def generate_answer(query, search_results):
    """Same as before but simplified"""
    if not search_results:
        return "I couldn't find information about this issue. Please consult a certified technician.", []
    
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
    answer_parts.append("⚠️ **SAFETY FIRST:** Always turn off power before inspection. Wear safety gear.")
    
    if search_results:
        answer_parts.append(f"**From manual:** {search_results[0]['text'][:300]}...")
    
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
    
    answer_parts.append("\n**Call certified technician if:**")
    answer_parts.append("- Problem persists after basic checks")
    answer_parts.append("- Safety circuit is faulting")
    answer_parts.append("- Electrical components are damaged")
    
    return "\n\n".join(answer_parts), search_results

def ask_question(query):
    """Main function"""
    try:
        # Load chunks
        with open("Data/chunks.txt", "r", encoding="utf-8") as f:
            chunks = [line.strip() for line in f if line.strip()]
    except:
        chunks = []
    
    # Search
    search_results = simple_search(query, chunks)
    
    # Generate answer
    answer, sources = generate_answer(query, search_results)
    
    return answer, sources

if __name__ == "__main__":
    print("🛗 ELEVATOR MAINTENANCE ASSISTANT")
    query = input("\nDescribe the issue: ")
    answer, sources = ask_question(query)
    print("\n" + "="*50)
    print(answer)