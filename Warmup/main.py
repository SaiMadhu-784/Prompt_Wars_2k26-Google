import streamlit as st
import google.generativeai as genai
import os
import json
from PIL import Image
from dotenv import load_dotenv

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Universal Intent Bridge",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- PREMIUM CUSTOM STYLING (HACKATHON VIBE) ---
st.markdown("""
<style>
    /* Sleek Dark Background */
    .stApp {
        background-color: #0b0f19;
    }
    
    /* Gradient Title */
    h1 {
        background: -webkit-linear-gradient(45deg, #ff007f, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 800;
        padding-bottom: 0px;
    }
    
    p.subtitle {
        text-align: center;
        color: #a0aec0;
        font-size: 1.2rem;
        margin-bottom: 40px;
    }

    /* Vibrant Primary Button */
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #ff007f, #00f2fe);
        border: none;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        transition: transform 0.2s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.02);
        color: white !important;
        border: none;
    }
    
    /* Metrics Highlighting */
    div[data-testid="stMetricValue"] {
        background: -webkit-linear-gradient(45deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }
</style>
""", unsafe_allow_html=True)

# --- API KEY CONFIGURATION ---
load_dotenv()
env_api_key = os.getenv("GOOGLE_API_KEY")

with st.sidebar:
    st.markdown("### 🔑 API Authentication")
    st.markdown("To interact with the backend models securely without exposing tokens, please provide your **Google API Key** below.")
    
    API_KEY = st.text_input(
        "Google API Key",
        value=env_api_key if env_api_key and "your_actual" not in env_api_key.lower() else "",
        type="password",
        placeholder="AIza...",
        help="Get this from Google AI Studio. It stays in your browser memory and is never saved."
    )
    
    st.markdown("---")
    st.markdown("*Built for Prompt Wars 2k26-Google*")

if not API_KEY:
    st.warning("⚠️ **Authentication Required**: Please provide your Google API Key in the left sidebar to unlock the Universal Intent Bridge.")
    st.stop()

# Configure the Gemini SDK
genai.configure(api_key=API_KEY)

# Use 'gemini-2.5-flash' for extremely fast text/image multi-modal processing
model = genai.GenerativeModel(
    'gemini-2.5-flash',
    generation_config={"response_mime_type": "application/json"}
)

# --- SYSTEM INSTRUCTIONS ---
# Forcing structured JSON output from chaotic inputs
SYSTEM_PROMPT = """
You are the "Universal Intent Bridge" AI core. 
You act as a critical emergency and societal translator. 
Your primary goal is to accept completely unstructured, messy, chaotic real-world data (like panicked voice transcripts, chaotic traffic feeds, cryptic medical notes, blurry photos, or severe weather reports) and instantly convert them into a structured, verified, and life-saving Action Plan.

Output EXACTLY in this JSON schema:
{
  "category": "Medical|Traffic|Weather|Security|General",
  "urgency_level": "CRITICAL|HIGH|MODERATE|LOW",
  "summary": "1-sentence verified summary of the core situation",
  "key_entities": ["list", "of", "important", "factors", "extracted"],
  "immediate_actions": [
    {"step": 1, "action": "Clear directive", "target_agency": "Who needs to act (e.g. Police, EMS, User)"}
  ]
}
"""

# --- UI LAYOUT ---
st.markdown("<h1>Universal Intent Bridge 🌌</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Transforming chaotic, unstructured real-world data into verified life-saving actions instantly.</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📥 Unstructured Input Feed")
    st.markdown("Drop messy texts, voice transcripts, or upload chaotic visuals.")
    
    input_text = st.text_area("Messy Transcript / Notes", height=150, placeholder="e.g. \"Massive pile-up on highway 9! Terrible weather, need EMS now, wait I think someone is trapped...\"")
    uploaded_file = st.file_uploader("Upload Evidence (Image/Medical Scan etc)", type=["png", "jpg", "jpeg"])
    
    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Visual Data", use_container_width=True)
    
    analyze_btn = st.button("🚀 Transform to Actions", use_container_width=True)

with col2:
    st.subheader("💡 Verified Structured Output")
    
    if analyze_btn:
        if not input_text and not image:
            st.warning("⚠️ Please provide either unstructured text or an image evidence to analyze.")
        else:
            with st.spinner("Bridging Intent... Integrating Real-World Data..."):
                try:
                    contents = [SYSTEM_PROMPT]
                    if input_text:
                        contents.append(f"Unstructured Raw Data: {input_text}")
                    if image:
                        contents.append(image)
                    
                    response = model.generate_content(contents)
                    result = json.loads(response.text)
                    
                    # 1. Metrics Layout
                    m1, m2 = st.columns(2)
                    m1.metric("📌 Category", result.get("category", "Unknown"))
                    
                    urgency = result.get("urgency_level", "Unknown")
                    if urgency in ["CRITICAL", "HIGH"]:
                        m2.error(f"🚨 Urgency: {urgency}")
                    elif urgency == "MODERATE":
                        m2.warning(f"⚠️ Urgency: {urgency}")
                    else:
                        m2.info(f"✅ Urgency: {urgency}")
                    
                    # 2. Executive Summary
                    st.success(f"**Verified Summary:** {result.get('summary', '')}")
                    
                    # 3. Key Entities
                    st.markdown("### 🔑 Key Entities Detected")
                    st.code(", ".join(result.get("key_entities", [])), language="text")
                    
                    # 4. Action Directives
                    st.markdown("### ⚡ Live Action Directives")
                    for action in result.get("immediate_actions", []):
                        st.info(f"**Step {action.get('step')}:** {action.get('action')} ➔ _Assignee:_ **{action.get('target_agency')}**")
                        
                except Exception as e:
                    st.error(f"Failed to bridge intent: {str(e)}")
    else:
        st.info("Awaiting messy input stream on the left...")