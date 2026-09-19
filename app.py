import streamlit as st
from groq import Groq

# 1. Page Config (Wide Layout for Website Feel)
st.set_page_config(page_title="AI Content Pro", page_icon="🚀", layout="wide", initial_sidebar_state="collapsed")

# 2. Custom CSS for UI/UX Styling
st.markdown("""
    <style>
    /* Main background and font adjustments */
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1000px; }
    
    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #2E86C1;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { background-color: #1B4F72; border-color: #1B4F72; color: white; }
    
    /* Card-like containers */
    div[data-testid="stForm"] {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Try to load API Key safely
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("⚠️ API Key missing in Streamlit Secrets!")
    st.stop()

client = Groq(api_key=groq_api_key)

# 3. Hero Section (Website Header)
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🚀 AI Content Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #555;'>Your smart assistant for multi-platform content, SEO, and engagement.</p>", unsafe_allow_html=True)
st.divider()

# 4. Interactive Layout using Columns
col_settings, col_input = st.columns([1, 2], gap="large")

with col_settings:
    st.subheader("⚙️ Content Strategy")
    platform = st.selectbox("Platform", ["LinkedIn", "Twitter/X", "Instagram", "YouTube (Shorts/Long-form)"])
    content_type = st.selectbox("Content Type", ["Informational Post", "Story/Experience", "Video Script/Hook", "Tutorial"])
    tone = st.selectbox("Tone", ["Professional", "Casual", "Inspirational", "Humorous", "Authoritative"])
    target_audience = st.text_input("Target Audience", placeholder="e.g., Software Engineers, Founders...")

with col_input:
    st.subheader("✍️ Draft Details")
    topic = st.text_area("What is the core topic or narrative?", placeholder="Briefly describe the story, hackathon win, or technical topic...", height=150)
    
    generate_btn = st.button("Generate Content ✨")

# 5. Generation & Output Display using Tabs
if generate_btn:
    if not topic.strip() or not target_audience.strip():
        st.warning("⚠️ Please provide both a topic and a target audience.")
    else:
        with st.spinner(f"Crafting highly engaging {platform} content..."):
            prompt = f"""
            Act as an expert Content Strategist and Copywriter.
            Create content for {platform}.
            
            Details:
            - Content Type: {content_type}
            - Topic: {topic}
            - Target Audience: {target_audience}
            - Tone: {tone}
            
            Provide the output in 3 sections:
            1. The main post/script (formatted beautifully).
            2. 3 alternative Hook/Title options for A/B testing.
            3. A list of highly relevant SEO tags/hashtags.
            """
            
            try:
                # Using your selected model
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a top-tier digital content strategist."},
                        {"role": "user", "content": prompt}
                    ],
                    model="openai/gpt-oss-120b", 
                    temperature=0.7,
                )
                
                result = chat_completion.choices[0].message.content
                
                st.success("✅ Content Generated Successfully!")
                
                # Organize output interactively in Tabs
                tab1, tab2 = st.tabs(["📄 Generated Content", "💾 Export"])
                
                with tab1:
                    st.markdown(result)
                    
                with tab2:
                    st.write("Save your generated content directly to your device.")
                    st.download_button(
                        label="⬇️ Download as Text File",
                        data=result,
                        file_name="generated_content.txt",
                        mime="text/plain"
                    )
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
