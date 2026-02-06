import streamlit as st
import google.generativeai as genai
import re

# Set page config for dark theme and professional layout
st.set_page_config(
    page_title="AI Content Alchemist",
    page_icon="🧙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme and professional styling
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stTextArea textarea {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #333;
    }
    .stButton button {
        background-color: #6200ea;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton button:hover {
        background-color: #3700b3;
    }
    .stHeader {
        color: #bb86fc;
    }
    .stSubheader {
        color: #03dac6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App Title
st.title("🧙 AI Content Alchemist")
st.markdown("Transform long articles or transcripts into viral content using AI!")

# API Key Input
st.header("API Configuration")
api_key = st.text_input(
    "Enter your Google API Key (required for generation):",
    type="password",
    placeholder="Paste your Google AI API key here..."
)

# Input Section
st.header("Input Your Content")
input_text = st.text_area(
    "Paste your long article or video transcript here:",
    height=200,
    placeholder="Enter text here..."
)

# Generate Button
if st.button("Generate Viral Content"):
    if not api_key.strip():
        st.error("Please enter your Google API key.")
    elif not input_text.strip():
        st.error("Please enter some text to generate content.")
    else:
        try:
            # Configure Gemini API
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Structured prompt for Gemini
            prompt = f"""
            Based on the following content, generate the following in a structured format. Be creative, engaging, and optimized for virality.

            **Twitter Threads:**
            Provide 5 catchy Twitter (X) threads. Each thread should be a series of 3-5 connected tweets (under 280 characters each), formatted as:
            Thread 1: [Tweet 1 text]\n[Tweet 2 text]\n[Tweet 3 text]\n...
            Thread 2: ...

            **TikTok/Reels Script:**
            Create a 60-second viral video script for TikTok/Reels. Include timestamps (e.g., 0-10s: Description), engaging hooks, and calls to action. Keep it concise and script-like.

            **YouTube Headlines:**
            Suggest 3 high-CTR (Click-Through Rate) headlines for YouTube videos. Make them sensational, curiosity-driven, and SEO-friendly.

            Content: {input_text}
            """
            
            # Generate response
            response = model.generate_content(prompt)
            generated_text = response.text
            
            # Parse the response into sections
            def parse_sections(text):
                sections = {}
                # Split by ** headers
                parts = re.split(r'\*\*(.*?)\*\*', text)
                for i in range(1, len(parts), 2):
                    key = parts[i].strip()
                    value = parts[i+1].strip() if i+1 < len(parts) else ""
                    sections[key] = value
                return sections
            
            sections = parse_sections(generated_text)
            
            # Display Twitter Threads
            if "Twitter Threads" in sections:
                st.header("📱 Twitter (X) Threads")
                threads_text = sections["Twitter Threads"]
                threads = re.split(r'Thread \d+:', threads_text)[1:]  # Split into individual threads
                for i, thread in enumerate(threads[:5], 1):  # Limit to 5
                    thread = thread.strip()
                    st.subheader(f"Thread {i}")
                    st.text_area(f"Thread {i}", value=thread, height=150, key=f"thread_{i}")
                    if st.button(f"Copy Thread {i}"):
                        st.copy_to_clipboard(thread)
                        st.success("Copied to clipboard!")
            
            # Display TikTok Script
            if "TikTok/Reels Script" in sections:
                st.header("🎥 TikTok/Reels Script (60s)")
                script = sections["TikTok/Reels Script"]
                st.text_area("Script", value=script, height=200, key="script")
                if st.button("Copy Script"):
                    st.copy_to_clipboard(script)
                    st.success("Copied to clipboard!")
            
            # Display YouTube Headlines
            if "YouTube Headlines" in sections:
                st.header("📺 YouTube Headlines")
                headlines_text = sections["YouTube Headlines"]
                headlines = re.findall(r'\d+\.\s*(.+)', headlines_text)  # Extract numbered headlines
                for i, headline in enumerate(headlines[:3], 1):  # Limit to 3
                    st.write(f"{i}. {headline}")
                    if st.button(f"Copy Headline {i}"):
                        st.copy_to_clipboard(headline)
                        st.success("Copied to clipboard!")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}. Check your API key or try again.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and Google's Gemini Pro.")
