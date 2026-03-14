import streamlit as st
import requests
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
import gdown
import time
from datetime import datetime
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# File download and setup
file_id = "1kSsKcuC4WRhjoPZBpI6LYoJUltp5P6Kg"
url = f"https://drive.google.com/uc?id={file_id}"
output = ".env"

gdown.download(url, output, quiet=False)

# Load environment variables
load_dotenv()

# Validate API keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not GEMINI_API_KEY:
    st.error("❌ GEMINI_API_KEY not found in .env file!")
    st.stop()
if not SERPER_API_KEY:
    st.error("❌ SERPER_API_KEY not found in .env file!")
    st.stop()

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-pro')

# Serper API configuration
SERPER_API_URL = "https://google.serper.dev/search"

# Custom CSS for futuristic design
st.markdown("""
<style>
    /* Import futuristic fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Main container */
    .main-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Neon text effects */
    .neon-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: neon-pulse 2s ease-in-out infinite;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        margin-bottom: 1rem;
    }
    
    @keyframes neon-pulse {
        0%, 100% { filter: brightness(1); }
        50% { filter: brightness(1.2); }
    }
    
    /* Glowing text */
    .glow-text {
        font-size: 1.2rem;
        color: #fff;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        animation: glow 2s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { text-shadow: 0 0 10px rgba(255, 255, 255, 0.5); }
        50% { text-shadow: 0 0 20px rgba(255, 255, 255, 0.8), 0 0 30px #4ecdc4; }
    }
    
    /* Futuristic cards */
    .futuristic-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: float 6s ease-in-out infinite;
    }
    
    .futuristic-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3), 0 0 20px #4ecdc4;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Cyber button */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        font-family: 'Orbitron', sans-serif;
        font-weight: bold;
        border: none;
        border-radius: 50px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        box-shadow: 0 0 20px rgba(78, 205, 196, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(78, 205, 196, 0.8);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Futuristic input */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(78, 205, 196, 0.3);
        border-radius: 10px;
        color: white;
        font-size: 1.1rem;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4ecdc4;
        box-shadow: 0 0 20px rgba(78, 205, 196, 0.3);
        outline: none;
    }
    
    /* Radio buttons styling */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50px;
        padding: 0.5rem;
    }
    
    .stRadio > div > label {
        color: white !important;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        background-size: 300% 100%;
        animation: gradient-shift 3s ease infinite;
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Metric cards */
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        flex: 1;
        margin: 0 0.5rem;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .metric-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 2rem;
        font-weight: bold;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Loading animation */
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
    }
    
    .loading-spinner::after {
        content: '';
        width: 50px;
        height: 50px;
        border: 5px solid rgba(255, 255, 255, 0.1);
        border-top-color: #4ecdc4;
        border-radius: 50%;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(45deg, #45b7d1, #96ceb4);
        color: white;
        font-family: 'Orbitron', sans-serif;
        border: none;
        border-radius: 50px;
        padding: 0.5rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(69, 183, 209, 0.5);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.9rem;
        margin-top: 3rem;
        padding: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Particle background */
    #particles-js {
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        z-index: -1;
    }
    
    /* Trending topics */
    .trending-tag {
        display: inline-block;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(78, 205, 196, 0.3);
        border-radius: 20px;
        padding: 0.3rem 1rem;
        margin: 0.3rem;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .trending-tag:hover {
        background: rgba(78, 205, 196, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(78, 205, 196, 0.3);
    }
    
    /* Voice assistant button */
    .voice-button {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        border: none;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        box-shadow: 0 0 20px rgba(78, 205, 196, 0.5);
        animation: pulse 2s ease-in-out infinite;
        z-index: 1000;
    }
    
    .voice-button:hover {
        transform: scale(1.1);
    }
    
    /* Timeline */
    .timeline-item {
        position: relative;
        padding-left: 30px;
        margin: 20px 0;
        border-left: 2px solid #4ecdc4;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -8px;
        top: 0;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: #4ecdc4;
        box-shadow: 0 0 10px #4ecdc4;
    }
    
    .timeline-date {
        font-family: 'Orbitron', sans-serif;
        color: #4ecdc4;
        font-size: 0.9rem;
    }
    
    .timeline-content {
        color: white;
        margin-top: 5px;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .neon-title {
            font-size: 2rem;
        }
        
        .metric-container {
            flex-direction: column;
        }
        
        .metric-card {
            margin: 0.5rem 0;
        }
        
        .voice-button {
            width: 50px;
            height: 50px;
            font-size: 1.2rem;
            bottom: 1rem;
            right: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Add particle animation background
st.markdown("""
<div id="particles-js"></div>
<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<script>
    particlesJS('particles-js', {
        particles: {
            number: { value: 80, density: { enable: true, value_area: 800 } },
            color: { value: '#4ecdc4' },
            shape: { type: 'circle' },
            opacity: { value: 0.5, random: true },
            size: { value: 3, random: true },
            line_linked: { enable: true, distance: 150, color: '#4ecdc4', opacity: 0.4, width: 1 },
            move: { enable: true, speed: 2, direction: 'none', random: true, straight: false, out_mode: 'out' }
        },
        interactivity: {
            detect_on: 'canvas',
            events: { onhover: { enable: true, mode: 'repulse' }, onclick: { enable: true, mode: 'push' } },
            modes: { repulse: { distance: 100, duration: 0.4 }, push: { particles_nb: 4 } }
        },
        retina_detect: true
    });
</script>
""", unsafe_allow_html=True)

def serper_search(query: str, num_results: int = 10) -> dict:
    """
    Perform a Google search using Serper API
    
    Args:
        query: Search query string
        num_results: Number of results to return
    
    Returns:
        Dictionary containing search results
    """
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "q": query,
        "num": num_results,
        "gl": "us",  # Country
        "hl": "en"   # Language
    }
    
    try:
        response = requests.post(SERPER_API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Serper API error: {e}")
        return {"error": str(e)}

# Add this alias to fix the search_google error
search_google = serper_search

# Add this after your search_google alias
class SerperClient:
    def search(self, query, max_results=3, topic="general"):
        # Convert parameters to match your search_google function
        return search_google(query, num_results=max_results)

serper_client = SerperClient()

# Select the model
MODEL_INFO = "gemini-2.5-flash"  # Changed from gemini-2.0-flash to a valid model
MODEL_SCRIPT = "gemini-2.5-flash"  # Changed from gemini-2.0-flash to a valid model

st.set_page_config(
    page_title="StoryForge AI - Future of Content Creation", 
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": "https://www.google.com",
        "Report a bug": "https://www.google.com",
        "About": "StoryForge AI - The future of content creation with cutting-edge AI technology."
    }
)

# Initialize session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'current_theme' not in st.session_state:
    st.session_state.current_theme = 'dark'

def get_realtime_info(query):
    """
    Fetches up-to-date information about any topic using Serper API
    and summarizes it using Gemini.
    """
    try:
        resp = serper_client.search(
            query=query,
            max_results=5,
            topic="general"
        )

        # Check for organic results (Serper API returns results in "organic" array)
        if resp and "organic" in resp and resp["organic"]:
            summaries = []
            for r in resp["organic"][:5]:  # Get top 5 results
                title = r.get("title", "No title")
                snippet = r.get("snippet", "No description available")
                link = r.get("link", "#")  # Serper uses "link" not "url"
                summaries.append(f"**{title}**\n\n{snippet}\n\n🔗 {link}")
            source_info = "\n\n---\n\n".join(summaries)
        else:
            source_info = f"No recent updates found on '{query}'."
            
    except Exception as e:
        st.error(f"❌ Error fetching info: {e}")
        return None

    # Refine & summarize the content via Gemini
    prompt = f"""
You are a professional researcher and social media content creator with expertise in multiple fields.
Using the following real-time information, write an accurate, engaging, and human-like summary
for the topic: '{query}'.

Requirements:
- Keep it factual, insightful, and concise (around 200 words).
- Maintain a smooth, natural tone.
- Highlight key takeaways or trends.
- Include a "Key Insights" section with bullet points.
- Add a "Future Outlook" section predicting trends.
- Avoid greetings or self-references.

Source information:
{source_info}

Output only the refined, human-readable content.
"""

    try:
        model = genai.GenerativeModel(MODEL_INFO)
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else source_info
    except Exception as e:
        st.error(f"❌ Error generating summary: {e}")
        return source_info

def generate_video_script(info_text, style="viral"):
    style_prompts = {
        "viral": "Use an energetic, fast-paced style with trending sounds and effects. Include timestamps for sound effects.",
        "educational": "Focus on clear explanations, use diagrams and text overlays. Break down complex concepts.",
        "storytelling": "Create a narrative arc with emotional hooks. Use music cues and dramatic pauses.",
        "humorous": "Incorporate comedy timing, meme references, and lighthearted moments."
    }
    
    prompt = f"""
You are a creative scriptwriter.
Turn this real-time information into an engaging short video script (for YouTube Shorts or Instagram Reels).
Style: {style_prompts.get(style, style_prompts['viral'])}

Requirements:
- Strong hook in first 3 seconds
- Timestamps for key moments
- Visual effect suggestions
- Sound effect cues
- Clear call to action
- Hashtag suggestions at the end
- Keep it around 100–120 words

Format with [SFX] for sound effects and [VISUAL] for visual cues.

Content to base script on:
{info_text}
"""
    try:
        model = genai.GenerativeModel(MODEL_SCRIPT)
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else "⚠️ Could not generate video script."
    except Exception as e:
        st.error(f"❌ Error generating video script: {e}")
        return None

def generate_content_ideas(topic):
    prompt = f"""
Generate 5 creative content ideas based on: {topic}

For each idea, include:
1. Catchy title
2. Brief description
3. Target audience
4. Best platform (YouTube, TikTok, Instagram, LinkedIn)
5. Estimated engagement potential (High/Medium/Low)

Format as a list with clear sections.
"""
    try:
        model = genai.GenerativeModel(MODEL_INFO)
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else "No ideas generated."
    except Exception as e:
        return f"Error: {e}"

def generate_trend_analysis(query, info_text):
    prompt = f"""
Based on the following information about '{query}', provide a trend analysis:

{info_text}

Include:
1. Current trend direction (Rising/Peak/Declining)
2. Key drivers behind the trend
3. Related topics gaining traction
4. Predicted trajectory for next 3 months
5. Recommended action for content creators

Format with clear sections and bullet points.
"""
    try:
        model = genai.GenerativeModel(MODEL_INFO)
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else "Analysis unavailable."
    except Exception as e:
        return f"Error: {e}"

def main():
    # Header with neon effect
    st.markdown('<h1 class="neon-title">🚀 STORYFORGE AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="glow-text" style="text-align:center;">The Future of Content Creation is Here</p>', unsafe_allow_html=True)
    
    # Metrics section
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">10K+</div>
            <div class="metric-label">Active Users</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">50K+</div>
            <div class="metric-label">Scripts Generated</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">98%</div>
            <div class="metric-label">Satisfaction Rate</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">24/7</div>
            <div class="metric-label">AI Support</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Trending topics section
    st.markdown('<p class="glow-text" style="margin-top: 2rem;">🔥 Trending Topics</p>', unsafe_allow_html=True)
    trending_topics = ["AI Revolution", "Climate Tech", "Space Exploration", "Digital Art", "Metaverse", "Quantum Computing", "Green Energy", "Future of Work"]
    
    trending_html = '<div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 2rem;">'
    for topic in trending_topics:
        trending_html += f'<span class="trending-tag" onclick="navigator.clipboard.writeText(\'{topic}\')">#{topic}</span>'
    trending_html += '</div>'
    st.markdown(trending_html, unsafe_allow_html=True)
    
    # Main search section
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Search input with icon
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input("🔎 Enter your topic or question:", placeholder="e.g., Future of AI, Climate Change Solutions, Space Tourism...")
    with col2:
        search_type = st.selectbox("Search Type", ["General", "News", "Research", "Trending"], index=0)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if query:
        # Add to search history
        if query not in st.session_state.search_history:
            st.session_state.search_history.append(query)
        
        # Progress bar for visual effect
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        
        with st.spinner("🌍 Gathering latest information..."):
            info_result = get_realtime_info(query)
        
        if info_result:
            # Main content in futuristic card
            st.markdown('<div class="futuristic-card">', unsafe_allow_html=True)
            
            # Tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["📚 Summary", "📊 Trend Analysis", "💡 Content Ideas", "📈 Insights"])
            
            with tab1:
                st.subheader("AI-Generated Summary")
                st.write(info_result)
                
                # Add to favorites button
                col1, col2 = st.columns([1, 5])
                with col1:
                    if st.button("⭐ Add to Favorites"):
                        if query not in st.session_state.favorites:
                            st.session_state.favorites.append(query)
                            st.success("Added to favorites!")
                        else:
                            st.info("Already in favorites!")
            
            with tab2:
                st.subheader("Trend Analysis")
                trend_analysis = generate_trend_analysis(query, info_result)
                st.write(trend_analysis)
                
                # Sample trend chart
                dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
                trend_data = pd.DataFrame({
                    'Date': dates,
                    'Interest': [random.randint(50, 100) + i for i in range(30)]
                })
                
                fig = px.line(trend_data, x='Date', y='Interest', title='Interest Over Time')
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                st.subheader("Content Ideas")
                content_ideas = generate_content_ideas(query)
                st.write(content_ideas)
            
            with tab4:
                st.subheader("Key Insights")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div class="timeline-item">
                        <div class="timeline-date">Current Status</div>
                        <div class="timeline-content">Emerging trend with high potential</div>
                    </div>
                    <div class="timeline-item">
                        <div class="timeline-date">Next Week</div>
                        <div class="timeline-content">Expected to gain traction</div>
                    </div>
                    <div class="timeline-item">
                        <div class="timeline-date">Next Month</div>
                        <div class="timeline-content">Peak interest predicted</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Engagement metrics
                    metrics = {
                        'Views': '1.2M',
                        'Engagement': '85%',
                        'Shares': '45K',
                        'Comments': '12K'
                    }
                    
                    for label, value in metrics.items():
                        st.markdown(f"""
                        <div style="margin: 1rem 0;">
                            <div style="color: #4ecdc4;">{label}</div>
                            <div style="font-size: 1.5rem; font-weight: bold;">{value}</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Video script generation with style options
            st.markdown('<div class="futuristic-card">', unsafe_allow_html=True)
            st.subheader("🎬 Video Script Generator")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                generate_script = st.radio(
                    "Generate Script?",
                    ["No", "Yes"],
                    index=0,
                    horizontal=True
                )
            
            if generate_script == "Yes":
                with col2:
                    script_style = st.selectbox(
                        "Script Style",
                        ["viral", "educational", "storytelling", "humorous"],
                        index=0
                    )
                
                with st.spinner('🎥 Crafting your video script...'):
                    script = generate_video_script(info_result, script_style)
                
                if script:
                    st.write(script)
                    
                    # Download options
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.download_button(
                            label="📥 Download as TXT",
                            data=script,
                            file_name=f"script_{query[:20]}.txt",
                            mime="text/plain"
                        )
                    with col2:
                        if st.button("🎯 Copy to Clipboard"):
                            st.write("Script copied! (Simulated - would need JavaScript)")
                            st.balloons()
                    with col3:
                        if st.button("📤 Share"):
                            st.write("Sharing options (Simulated)")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Related topics
            st.markdown('<div class="futuristic-card">', unsafe_allow_html=True)
            st.subheader("🔗 Related Topics")
            related_topics = [f"{query} trends", f"{query} future", f"{query} impact", f"{query} statistics", f"{query} analysis"]
            
            related_html = '<div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">'
            for topic in related_topics:
                related_html += f'<span class="trending-tag" onclick="navigator.clipboard.writeText(\'{topic}\')">{topic}</span>'
            related_html += '</div>'
            st.markdown(related_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar with history and favorites
    with st.sidebar:
        st.markdown('<h3 style="color: #4ecdc4;">📜 History</h3>', unsafe_allow_html=True)
        if st.session_state.search_history:
            for i, item in enumerate(reversed(st.session_state.search_history[-5:])):
                if st.button(f"🔍 {item}", key=f"history_{i}"):
                    st.session_state.query = item
                    st.experimental_rerun()
        else:
            st.write("No search history yet")
        
        st.markdown('<h3 style="color: #4ecdc4; margin-top: 2rem;">⭐ Favorites</h3>', unsafe_allow_html=True)
        if st.session_state.favorites:
            for i, item in enumerate(st.session_state.favorites):
                st.write(f"⭐ {item}")
        else:
            st.write("No favorites yet")
        
        # Voice assistant button (simulated)
        st.markdown("""
        <button class="voice-button" onclick="alert('Voice assistant activated! (Demo)')">
            🎤
        </button>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="footer">', unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>© 2024 StoryForge AI - The Future of Content Creation</div>
        <div>
            <span style="margin: 0 1rem; cursor: pointer;">Privacy</span>
            <span style="margin: 0 1rem; cursor: pointer;">Terms</span>
            <span style="margin: 0 1rem; cursor: pointer;">Contact</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()