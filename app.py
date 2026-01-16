import streamlit as st
from qa import ask_question

# app.py - Simple Elevator Maintenance Assistant

# Page setup
st.set_page_config(
    page_title="Elevator AI Assistant",
    page_icon="🛗",
    layout="centered"
)

# Header
st.title("🛗 AI Elevator Maintenance Assistant")
st.markdown("Get instant guidance for elevator faults using AI search")

# Sidebar with info
with st.sidebar:
    st.header("How It Works")
    st.markdown("""
    **Two AI Components:**
    1. **Smart Search** - Finds relevant manual sections
    2. **Advice Generator** - Creates step-by-step guidance
    
    **Instructions:**
    1. Describe the problem
    2. Click 'Get Help'
    3. Follow safety steps first
    4. Check the manual sections found
    """)
    
    st.markdown("---")
    st.caption("Note: This is an assistant tool. Always follow official procedures.")

# Main area
st.subheader("Describe the Elevator Problem")

# User input
problem = st.text_area(
    "What's wrong with the elevator?",
    placeholder="Example: Door is making noise, Error code E5 showing, Elevator stuck between floors...",
    height=100
)

# Process button
if st.button("🔧 Get Maintenance Help", type="primary"):
    if problem:
        with st.spinner("Searching manual and generating advice..."):
            # Get answer from our system
            answer, sources = ask_question(problem)
        
        # Display results
        st.success("✅ Analysis Complete!")
        
        # Show the answer
        st.markdown("---")
        st.subheader("📋 Recommended Actions")
        st.markdown(answer)
        
        # Show the sources (PROOF OF AI COMPONENT 1)
        st.markdown("---")
        st.subheader("📖 Manual Sections Found")
        st.markdown("*(These were found by the AI search system)*")
        
        for i, source in enumerate(sources):
            with st.expander(f"Section {i+1} (Relevance: {source['similarity']:.2f}/1.0)"):
                st.markdown(source['text'])
                st.caption(f"Search distance: {source['distance']:.3f}")
        
        # Extra options
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 New Query"):
                st.rerun()
        with col2:
            st.download_button(
                "💾 Save This Advice",
                data=answer,
                file_name="elevator_advice.txt"
            )
    else:
        st.warning("Please describe the problem first!")

# Footer
st.markdown("---")
st.markdown("""
**System Info:**
- AI Search: Sentence Transformers + FAISS
- Manual Sections: {} chunks
- Safety-Focused: Always prioritizes safety steps
""")