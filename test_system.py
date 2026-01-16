from qa import ask_question

print("🧪 Testing Elevator AI System...")
print("=" * 50)


test_cases = [
    "door not closing",
    "error code E5", 
    "grinding noise",
    "elevator stuck"
]

for query in test_cases:
    print(f"\n🔍 Testing: '{query}'")
    try:
        answer, sources = ask_question(query)
        print(f"   ✓ Answer: {len(answer)} characters")
        print(f"   ✓ Sources found: {len(sources)}")
        if sources:
            print(f"   ✓ Best source relevance: {sources[0]['similarity']:.2f}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

# Additional edge case tests
edge_cases = [
    "",
    "xyz invalid query",
    "emergency stop button",
    "power failure",
    "cable tension"
]

print("\n" + "-" * 50)
print("🧪 Testing Edge Cases...")
for query in edge_cases:
    print(f"\n🔍 Testing: '{query}'")
    try:
        answer, sources = ask_question(query)
        print(f"   ✓ Answer: {len(answer)} characters")
        print(f"   ✓ Sources found: {len(sources)}")
        if not sources:
            print(f"   ⚠ No sources found")
        elif sources[0]['similarity'] < 0.5:
            print(f"   ⚠ Low relevance: {sources[0]['similarity']:.2f}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

print("\n" + "=" * 50)
print("✅ System test complete!")