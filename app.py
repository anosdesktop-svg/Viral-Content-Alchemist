import streamlit as st
import google.generativeai as genai

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
            
            # Try to use the specified model; fallback to listing models if error
            try:
                model = genai.GenerativeModel('gemini-2.5-flash-lite')  # User-specified model
            except Exception as model_error:
                st.warning(f"Model 'gemini-2.5-flash-lite' not available: {str(model_error)}. Attempting to list available models...")
                try:
                    models = genai.list_models()
                    available_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
                    st.info(f"Available models for generateContent: {', '.join(available_models)}")
                    if available_models:
                        model_name = available_models[0]  # Use the first available
                        st.info(f"Using model: {model_name}")
                        model = genai.GenerativeModel(model_name)
                    else:
                        raise Exception("No suitable models found.")
                except Exception as list_error:
                    st.error(f"Could not list models: {str(list_error)}. Please check your API key or library version.")
                    st.stop()
            
            # Updated structured prompt with strict markers
            prompt = f"""
            Based on the following content, generate the following in a strict format using the exact markers. Be creative, engaging, and optimized for virality. Always respond in the same language as the input text.

            [TWITTER]
            Provide 5 catchy Twitter (X) threads. Each thread should be a series of 3-5 connected tweets (under 280 characters each), formatted as:
            Thread 1: [Tweet 1 text]\n[Tweet 2 text]\n[Tweet 3 text]\n...
            Thread 2: ...

            [YOUTUBE]
            Suggest 3 high-CTR (Click-Through Rate) headlines for YouTube videos. Make them sensational, curiosity-driven, and SEO-friendly.

            [TIKTOK]
            Create a 60-second viral video script for TikTok/Reels. Include timestamps (e.g., 0-10s: Description), engaging hooks, and calls to action. Keep it concise and script-like.

            [SECTION_INSTAGRAM]
            Provide a viral Instagram Reel script and 5 trending hashtags.

            Content: {input_text}
            """
            
            # Generate response
            response = model.generate_content(prompt)
            generated_text = response.text
            
            # Robust parsing using simple string splitting
            def parse_sections(text):
                sections = {}
                # Split by markers
                if '[TWITTER]' in text and '[YOUTUBE]' in text and '[TIKTOK]' in text and '[SECTION_INSTAGRAM]' in text:
                    twitter_part = text.split('[TWITTER]')[1].split('[YOUTUBE]')[0].strip()
                    youtube_part = text.split('[YOUTUBE]')[1].split('[TIKTOK]')[0].strip()
                    tiktok_part = text.split('[TIKTOK]')[1].split('[SECTION_INSTAGRAM]')[0].strip()
                    instagram_part = text.split('[SECTION_INSTAGRAM]')[1].strip()
                    sections['Twitter Threads'] = twitter_part
                    sections['YouTube Headlines'] = youtube_part
                    sections['TikTok/Reels Script'] = tiktok_part
                    sections['Instagram Reel Script and Hashtags'] = instagram_part
                else:
                    # Fallback: try to extract if markers are missing or out of order
                    sections['Twitter Threads'] = "Content not found. Please try again."
                    sections['YouTube Headlines'] = "Content not found. Please try again."
                    sections['TikTok/Reels Script'] = "Content not found. Please try again."
                    sections['Instagram Reel Script and Hashtags'] = "Content not found. Please try again."
                return sections
            
            sections = parse_sections(generated_text)
            
            # Display Twitter Threads (always show)
            st.header("📱 Twitter (X) Threads")
            threads_text = sections.get('Twitter Threads', 'No content generated.')
            threads = threads_text.split('Thread ') if 'Thread ' in threads_text else [threads_text]
            threads = [t.strip() for t in threads if t.strip()][:5]  # Limit to 5
            for i, thread in enumerate(threads, 1):
                st.subheader(f"Thread {i}")
                st.text_area(f"Thread {i}", value=thread, height=150, key=f"thread_{i}")
                if st.button(f"Copy Thread {i}"):
                    st.copy_to_clipboard(thread)
                    st.success("Copied to clipboard!")
            
            # Display YouTube Headlines (always show)
            st.header("📺 YouTube Headlines")
            headlines_text = sections.get('YouTube Headlines', 'No content generated.')
            headlines = [h.strip() for h in headlines_text.split('\n') if h.strip()][:3]  # Limit to 3
            for i, headline in enumerate(headlines, 1):
                st.write(f"{i}. {headline}")
                if st.button(f"Copy Headline {i}"):
                    st.copy_to_clipboard(headline)
                    st.success("Copied to clipboard!")
            
            # Display TikTok Script (always show)
            st.header("🎥 TikTok/Reels Script (60s)")
            script = sections.get('TikTok/Reels Script', 'No content generated.')
            st.text_area("Script", value=script, height=200, key="script")
            if st.button("Copy Script"):
                st.copy_to_clipboard(script)
                st.success("Copied to clipboard!")
            
            # Display Instagram Reel Script and Hashtags (always show)
            st.header("📸 Instagram Reel Script and Hashtags")
            instagram_content = sections.get('Instagram Reel Script and Hashtags', 'No content generated.')
            st.text_area("Instagram Content", value=instagram_content, height=200, key="instagram")
            if st.button("Copy Instagram Content"):
                st.copy_to_clipboard(instagram_content)
                st.success("Copied to clipboard!")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}. Check your API key or try again.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and Google's Gemini.")
