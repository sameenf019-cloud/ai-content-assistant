import streamlit as st
from groq import Groq

# Set up the Streamlit page
st.set_page_config(page_title="AI Content Assistant", page_icon="📝", layout="centered")

st.title("📝 AI Content Assistant")
st.write("Generate social media posts with captions and hashtags instantly!")

# Attempt to load the Groq API key from Streamlit secrets
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.info("Please add your GROQ_API_KEY to the Streamlit secrets to run the app.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=groq_api_key)

# Sidebar inputs for content configuration
with st.sidebar:
    st.header("Content Settings")
    platform = st.selectbox("Platform", ["LinkedIn", "Twitter/X", "Instagram", "Facebook"])
    content_type = st.selectbox(
        "Content Type", 
        ["Informational Post", "Story/Experience", "Promotional", "Tutorial", "Engagement Question"]
    )
    tone = st.selectbox("Tone", ["Professional", "Casual", "Humorous", "Inspirational", "Authoritative"])
    target_audience = st.text_input("Target Audience", placeholder="e.g., Software Engineers, Founders")

# Main content area
topic = st.text_area("What should the post be about?", placeholder="Describe your topic briefly here...")

if st.button("Generate Content ✨"):
    if not topic.strip() or not target_audience.strip():
        st.warning("Please provide both a topic and a target audience.")
    else:
        with st.spinner("Generating your post..."):
            # Construct the prompt
            prompt = f"""
            Act as an expert Social Media Manager and Copywriter.
            Create a highly engaging post for {platform}.
            
            Details:
            - Content Type: {content_type}
            - Topic: {topic}
            - Target Audience: {target_audience}
            - Tone: {tone}
            
            The output must include:
            1. The complete post body/caption formatted for {platform}.
            2. Highly relevant and trending hashtags at the end.
            """
            
            try:
                # Call the Groq API using the high-speed Llama 3.3 70B model
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a top-tier social media content creator."},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama3-70b-8192", 
                    temperature=0.7,
                )
                
                # Display the result
                st.subheader("Your Generated Post:")
                generated_post = chat_completion.choices[0].message.content
                st.write(generated_post)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
