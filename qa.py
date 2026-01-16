import os

# qa.py - SUPER SIMPLE version

def load_chunks():
    """Load text chunks"""
    try:
        with open("Data/chunks.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def simple_search(query, chunks):
    """Simple keyword search"""
    if not chunks:
        return []
    
    query_lower = query.lower()
    results = []
    
    for chunk in chunks:
        chunk_lower = chunk.lower()
        # Simple word matching
        matching_words = sum(1 for word in query_lower.split() 
                           if len(word) > 3 and word in chunk_lower)
        if matching_words > 0:
            results.append({
                "text": chunk[:300],  # First 300 chars
                "score": matching_words
            })
    
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:2]

def generate_advice(query, results):
    """Generate maintenance advice"""
    if not results:
        return """⚠️ **SAFETY FIRST:** Turn off power, wear protective gear.
        
**General Steps:**
1. Visual inspection
2. Check safety devices
3. Consult manual
4. Call technician if needed""", []
    
    # Basic advice based on keywords
    advice = "⚠️ **SAFETY FIRST:** Turn off power, wear protective gear.\n\n"
    advice += f"**From manual:** {results[0]['text']}...\n\n"
    
    if "door" in query.lower():
        advice += """**For door issues:**
1. Check door sensors
2. Clean door tracks
3. Test safety edges
4. Verify alignment"""
    elif "noise" in query.lower():
        advice += """**For noise issues:**
1. Identify noise source
2. Check lubrication
3. Inspect guides
4. Tighten components"""
    else:
        advice += """**General maintenance:**
1. Visual inspection
2. Check all connections
3. Test safety circuits
4. Document findings"""
    
    return advice, results

def ask_question(query):
    """Main function"""
    chunks = load_chunks()
    results = simple_search(query, chunks)
    return generate_advice(query, results)