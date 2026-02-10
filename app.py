import streamlit as st
import google.generativeai as genai

# Set page config for cinematic studio theme
st.set_page_config(
    page_title="AI Content Alchemist",
    page_icon="🧙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for cinematic studio aesthetic with glassmorphism and neon effects
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    /* Dark cinematic background with cyberpunk studio placeholder */
    .stApp {
        background: url('https://source.unsplash.com/1600x900/?cyberpunk-studio,digital-art') no-repeat center center fixed;
        background-size: cover;
        color: #ffffff;
        font-family: 'Orbitron', sans-serif;
    }
    
    /* Glassmorphism card for inputs and outputs */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    }
    
    /* Neon Cyan/Purple glow for Generate button */
    .stButton button {
        background: linear-gradient(90deg, #00ffff, #8000ff);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        box-shadow: 0 0 15px #00ffff, 0 0 15px #8000ff;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        box-shadow: 0 0 25px #00ffff, 0 0 25px #8000ff;
        transform: scale(1.05);
    }
    
    /* Styling for inputs and headers */
    .stTextInput input, .stTextArea textarea, .stMultiselect {
        background-color: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
    }
    h1, h3 {
        color: #ffffff;
        text-shadow: 0 0 5px #00ffff;
    }
    
    /* Floating monitor style for right column */
    .floating-monitor {
        background: rgba(0, 0, 0, 0.8);
        border: 2px solid #00ffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 20px #00ffff;
        backdrop-filter: blur(10px);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App Title
st.title("🧙 AI Content Alchemist")
st.markdown("Transform long articles or transcripts into viral content using AI!")

# Layout using st.columns([1, 1.5])
col1, col2 = st.columns([1, 1.5])

with col1:
    # Left Column: Inputs inside glassmorphism card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("API Configuration")
    api_key = st.text_input(
        "Enter your Google API Key (required for generation):",
        type="password",
        placeholder="Paste your Google AI API key here..."
    )
    
    st.header("Select Platforms")
    platforms = ['Twitter', 'YouTube', 'TikTok', 'Instagram', 'Article']
    selected_platforms = st.multiselect(
        "Choose the platforms you want to generate content for:",
        options=platforms,
        default=platforms,  # Default to all selected
        help="Select one or more platforms. Only selected platforms will be generated."
    )
    
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
        elif not selected_platforms:
            st.error("Please select at least one platform.")
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
                
                # Build prompt dynamically based on selected platforms
                prompt = f"Based on the following content, generate the following in a strict format using the exact markers. Be creative, engaging, and optimized for virality. Always respond in the same language as the input text.\n\n"
                
                section_markers = {
                    'Twitter': "[TWITTER]\nProvide 5 catchy Twitter (X) threads. Each thread should be a series of 3-5 connected tweets (under 280 characters each), formatted as:\nThread 1: [Tweet 1 text]\n[Tweet 2 text]\n[Tweet 3 text]\n...\nThread 2: ...\n\n",
                    'YouTube': "[YOUTUBE]\nSuggest 3 high-CTR (Click-Through Rate) headlines for YouTube videos. Make them sensational, curiosity-driven, and SEO-friendly.\n\n",
                    'TikTok': "[TIKTOK]\nCreate a 60-second viral video script for TikTok/Reels. Include timestamps (e.g., 0-10s: Description), engaging hooks, and calls to action. Keep it concise and script-like.\n\n",
                    'Instagram': "[SECTION_INSTAGRAM]\nProvide a viral Instagram Reel script and 5 trending hashtags.\n\n",
                    'Article': "[SECTION_ARTICLE]\nGenerate a professional, well-structured long-form article based on the input content.\n\n"
                }
                
                for platform in selected_platforms:
                    prompt += section_markers[platform]
                
                prompt += f"Content: {input_text}"
                
                # Generate response
                response = model.generate_content(prompt)
                generated_text = response.text
                
                # Robust parsing using simple string splitting
                def parse_sections(text, selected_platforms):
                    sections = {}
                    marker_map = {
                        'Twitter': '[TWITTER]',
                        'YouTube': '[YOUTUBE]',
                        'TikTok': '[TIKTOK]',
                        'Instagram': '[SECTION_INSTAGRAM]',
                        'Article': '[SECTION_ARTICLE]'
                    }
                    # Extract sections based on selected platforms
                    for i, platform in enumerate(selected_platforms):
                        marker = marker_map[platform]
                        if marker in text:
                            start = text.find(marker) + len(marker)
                            if i + 1 < len(selected_platforms):
                                next_marker = marker_map[selected_platforms[i+1]]
                                end = text.find(next_marker)
                                if end != -1:
                                    sections[platform] = text[start:end].strip()
                                else:
                                    sections[platform] = text[start:].strip()
                            else:
                                sections[platform] = text[start:].strip()
                        else:
                            sections[platform] = "Content not found. Please try again."
                    return sections
                
                sections = parse_sections(generated_text, selected_platforms)
                
                # Store sections in session state for display in right column
                st.session_state['sections'] = sections
                st.session_state['generated'] = True
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}. Check your API key or try again.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Right Column: Floating Monitor for results
    st.markdown('<div class="floating-monitor">', unsafe_allow_html=True)
    st.header("Generated Content Monitor")
    if 'generated' in st.session_state and st.session_state['generated']:
        sections = st.session_state['sections']
        for platform in selected_platforms:
            st.subheader(f"📱 {platform} Content" if platform == 'Twitter' else f"📺 {platform} Content" if platform == 'YouTube' else f"🎥 {platform} Content" if platform == 'TikTok' else f"📸 {platform} Content" if platform == 'Instagram' else f"📄 {platform} Content")
            content = sections.get(platform, 'No content generated.')
            if platform == 'Twitter':
                threads = content.split('Thread ') if 'Thread ' in content else [content]
                threads = [t.strip() for t in threads if t.strip()][:5]  # Limit to 5
                for i, thread in enumerate(threads, 1):
                    st.write(f"Thread {i}:")
                    st.text_area(f"Thread {i}", value=thread, height=150, key=f"thread_{i}")
            elif platform == 'YouTube':
                headlines = [h.strip() for h in content.split('\n') if h.strip()][:3]  # Limit to 3
                for i, headline in enumerate(headlines, 1):
                    st.write(f"{i}. {headline}")
            elif platform == 'TikTok':
                st.text_area("Script", value=content, height=200, key="script")
            elif platform == 'Instagram':
                st.text_area("Instagram Content", value=content, height=200, key="instagram")
            elif platform == 'Article':
                st.text_area("Article", value=content, height=400, key="article")
    else:
        st.write("Generate content to see results here.")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and Google's Gemini.")
