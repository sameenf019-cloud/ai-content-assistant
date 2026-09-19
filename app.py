import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="AI Content Studio Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom Professional CSS (No emojis)
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }
    
    .nav-header {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: #ffffff;
        margin-bottom: 2rem;
        border: 1px solid #334155;
    }
    .nav-header h1 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .nav-header p {
        margin: 0.3rem 0 0 0;
        color: #94a3b8;
        font-size: 0.95rem;
    }

    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #2563eb;
        color: #ffffff;
        border: none;
        padding: 0.6rem 1rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        color: #ffffff;
        border: none;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 6px;
        padding: 0 16px;
        background-color: #0f172a;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563eb;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Session History State Initialization
if "history" not in st.session_state:
    st.session_state.history = []

# 4. API Key Access
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("GROQ_API_KEY is missing in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=groq_api_key)

# 5. Sidebar - Session History Log
with st.sidebar:
    st.title("Drafts History")
    st.caption("Access previously generated content from this session.")
    
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()

    st.divider()

    if not st.session_state.history:
        st.info("No saved drafts yet.")
    else:
        for idx, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"{item['platform']} - {item['topic'][:20]}..."):
                st.caption(f"Target: {item['audience']}")
                st.text_area("Saved Output", value=item['output'], height=120, key=f"hist_{idx}")

# 6. Main Navbar Header
st.markdown("""
    <div class="nav-header">
        <h1>AI Content Studio Pro</h1>
        <p>Enterprise social media generation, YouTube script planning, and SEO optimization workspace.</p>
    </div>
""", unsafe_allow_html=True)

# 7. Form Layout & Controls
col_settings, col_input = st.columns([1, 2], gap="large")

with col_settings:
    st.subheader("Content Strategy")
    platform = st.selectbox("Platform", ["LinkedIn", "Twitter/X", "Instagram", "YouTube (Shorts/Long-form)"])
    
    if platform == "YouTube (Shorts/Long-form)":
        content_type = st.selectbox("Content Type", ["Full Script with Scene Breakdown", "Video Hook & Intro", "SEO Metadata & Titles"])
    else:
        content_type = st.selectbox("Content Type", ["Informational Post", "Story/Experience", "Promotional", "Tutorial"])
        
    tone = st.selectbox("Tone", ["Professional", "Casual", "Inspirational", "Humorous", "Authoritative"])
    target_audience = st.text_input("Target Audience", placeholder="e.g., Software Engineers, Founders, Tech Enthusiasts")

with col_input:
    st.subheader("Draft Details")
    topic = st.text_area("Core Topic or Narrative Context", placeholder="Describe your topic, case study, story, or video prompt in detail...", height=140)
    
    include_visuals = False
    if platform == "YouTube (Shorts/Long-form)":
        include_visuals = st.checkbox("Include Scene-by-Scene Visual Prompts for AI Video Generators", value=True)
        
    generate_btn = st.button("Generate Content")

# 8. Generation Processing
if generate_btn:
    if not topic.strip() or not target_audience.strip():
        st.warning("Please provide both a topic and a target audience.")
    else:
        with st.spinner("Generating content..."):
            
            if platform == "YouTube (Shorts/Long-form)":
                prompt = f"""
                Act as an elite YouTube Content Director and Scriptwriter.
                Produce production-ready content for YouTube.

                Details:
                - Output Format: {content_type}
                - Topic: {topic}
                - Target Audience: {target_audience}
                - Tone: {tone}
                - Include Visual Prompts for Scene Generation: {include_visuals}

                Structure the output in clearly labeled sections:
                SECTION 1: SCRIPT & SCENE BREAKDOWN
                (Provide timestamps/scene numbers, Voiceover transcript, and Visual Prompts for AI video tools if requested).

                SECTION 2: TITLE A/B TESTING OPTIONS
                (3 high-CTR title variations tailored for YouTube ranking).

                SECTION 3: SEO METADATA
                (Optimized video description hook, top tags, and hashtags).
                """
            else:
                prompt = f"""
                Act as an expert Social Media Strategist and Copywriter.
                Create high-performing content for {platform}.

                Details:
                - Content Type: {content_type}
                - Topic: {topic}
                - Target Audience: {target_audience}
                - Tone: {tone}

                Structure the output in clearly labeled sections:
                SECTION 1: MAIN POST CONTENT
                (Formatted for {platform} reading behavior).

                SECTION 2: TITLE / HOOK VARIATIONS
                (3 alternative hook options for engagement testing).

                SECTION 3: SEO HASHTAGS & TAGS
                (Targeted and high-relevance hashtags).
                """

            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are an enterprise AI copywriter and content strategist."},
                        {"role": "user", "content": prompt}
                    ],
                  model="openai/gpt-oss-120b",
                    temperature=0.7,
                )
                
                output_text = chat_completion.choices[0].message.content
                
                # Save item to Session History
                st.session_state.history.append({
                    "platform": platform,
                    "topic": topic,
                    "audience": target_audience,
                    "output": output_text
                })

                st.success("Content generated and saved to session history!")

                # Output Tabs
                tab_preview, tab_copy, tab_export = st.tabs(["Formatted Preview", "Quick Copy Code", "Export File"])

                with tab_preview:
                    st.markdown(output_text)

                with tab_copy:
                    st.caption("Click the top-right copy icon inside the box below to copy the full output in one click.")
                    st.code(output_text, language="markdown")

                with tab_export:
                    st.write("Download the generated text document for local editing.")
                    st.download_button(
                        label="Download as Text File",
                        data=output_text,
                        file_name=f"{platform.lower().split()[0]}_content.txt",
                        mime="text/plain"
                    )

            except Exception as e:
                st.error(f"An error occurred: {e}")
