import streamlit as st
import google.generativeai as genai

# Add the new CSS styling block
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0E1117;
    }
    body {
        color: #FFFFFF;
    }
    .stButton button {
        background: linear-gradient(to right, #7f00ff, #e100ff);
        font-weight: bold;
        border-radius: 10px;
    }
    .stTextInput input {
        border: 1px solid #7f00ff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add the new page config
st.set_page_config(page_title='Gen Z AI', layout='wide')

# Add the new CSS styling block
st.markdown(
    """
    <style>
    /* Professional Dark Mode Background */
    body {
        background-color: #0e1117;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin: 0;
        padding: 0;
    }
    
    /* Style buttons with gradient (Purple/Blue) and rounded corners */
    .stButton button {
        background: linear-gradient(45deg, #6200ea, #03dac6);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton button:hover {
        background: linear-gradient(45deg, #3700b3, #018786);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* Style text areas with a sleek dark border */
    .stTextArea textarea {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 2px solid #333;
        border-radius: 8px;
        padding: 10px;
        transition: border-color 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #6200ea;
        outline: none;
    }
    
    /* Glassmorphism effect for cards and containers */
    .stExpander, .stContainer, .stMarkdown {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add professional CSS styling for dark theme and enhancements
st.markdown(
    """
    <style>
    /* Professional Dark Theme Background */
    body {
        background-color: #0e1117;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin: 0;
        padding: 0;
        animation: fadeIn 1s ease-in-out;
    }
    
    /* Fade-in animation for the entire page */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Style all buttons with gradient background, rounded corners, and hover effect */
    .stButton button {
        background: linear-gradient(45deg, #6200ea, #03dac6);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton button:hover {
        background: linear-gradient(45deg, #3700b3, #018786);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* Customize Text Input and Text Area boxes */
    .stTextInput input, .stTextArea textarea {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #4f4f4f;
        border-radius: 5px;
        padding: 10px;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6200ea;
        box-shadow: 0 0 8px rgba(98, 0, 234, 0.5);
        outline: none;
    }
    
    /* Style Titles (h1) and Subheaders (h3) */
    h1 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #ffffff;
        font-weight: 600;
        margin-bottom: 20px;
    }
    h3 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #c0c0c0; /* Silver color */
        font-weight: 500;
        margin-bottom: 15px;
    }
    
    /* Additional tweaks for overall professionalism */
    .stMarkdown {
        color: #ffffff;
    }
    .stExpander {
        background-color: #1e1e1e;
        border: 1px solid #333;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

# Platform Selection
st.header("Select Platforms")
platforms = ['Twitter', 'YouTube', 'TikTok', 'Instagram', 'Article']
selected_platforms = st.multiselect(
    "Choose the platforms you want to generate content for:",
    options=platforms,
    default=platforms,  # Default to all selected
    help="Select one or more platforms. Only selected platforms will be generated."
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
            
            # Display content for each selected platform using expanders
            for platform in selected_platforms:
                with st.expander(f"📱 {platform} Content" if platform == 'Twitter' else f"📺 {platform} Content" if platform == 'YouTube' else f"🎥 {platform} Content" if platform == 'TikTok' else f"📸 {platform} Content" if platform == 'Instagram' else f"📄 {platform} Content"):
                    content = sections.get(platform, 'No content generated.')
                    if platform == 'Twitter':
                        threads = content.split('Thread ') if 'Thread ' in content else [content]
                        threads = [t.strip() for t in threads if t.strip()][:5]  # Limit to 5
                        for i, thread in enumerate(threads, 1):
                            st.subheader(f"Thread {i}")
                            st.text_area(f"Thread {i}", value=thread, height=150, key=f"thread_{i}")
                            if st.button(f"Copy Thread {i}", key=f"copy_thread_{i}"):
                                st.copy_to_clipboard(thread)
                                st.success("Copied to clipboard!")
                    elif platform == 'YouTube':
                        headlines = [h.strip() for h in content.split('\n') if h.strip()][:3]  # Limit to 3
                        for i, headline in enumerate(headlines, 1):
                            st.write(f"{i}. {headline}")
                            if st.button(f"Copy Headline {i}", key=f"copy_headline_{i}"):
                                st.copy_to_clipboard(headline)
                                st.success("Copied to clipboard!")
                    elif platform == 'TikTok':
                        st.text_area("Script", value=content, height=200, key="script")
                        if st.button("Copy Script", key="copy_script"):
                            st.copy_to_clipboard(content)
                            st.success("Copied to clipboard!")
                    elif platform == 'Instagram':
                        st.text_area("Instagram Content", value=content, height=200, key="instagram")
                        if st.button("Copy Instagram Content", key="copy_instagram"):
                            st.copy_to_clipboard(content)
                            st.success("Copied to clipboard!")
                    elif platform == 'Article':
                        st.text_area("Article", value=content, height=400, key="article")
                        if st.button("Copy Article", key="copy_article"):
                            st.copy_to_clipboard(content)
                            st.success("Copied to clipboard!")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}. Check your API key or try again.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and Google's Gemini.")
