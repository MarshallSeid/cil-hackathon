import streamlit as st
from openai import OpenAI

# langchain 
from langchain_community.document_loaders import YoutubeLoader

# Initialize OpenAI client
client = None

def initialize_openai_client():
    global client
    api_key = st.secrets["OPENAI_TOKEN"]
    if api_key:
        client = OpenAI(api_key=api_key)

# API Key input
initialize_openai_client()

def generate_claims(input_text):
    if not client:
        st.error("Please enter your OpenAI API key to generate claims.")
        return None
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Analyze the following text and identify the main claims:"},
                {"role": "user", "content": input_text}
            ],
            stream=False,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def generate_offensive_messaging(input_text):
    # Placeholder function - replace with actual implementation
    return f"Potentially offensive message based on: {input_text}"

st.title("AAPI Countering Disinformation")

# Input field and button
input_text = st.text_input("Input - ex: Youtube Link")
transcript = ''

if st.button('load transcript'): 
    try: 
        loader = YoutubeLoader.from_youtube_url(input_text, add_video_info=False,language=["en", "id","hi"],translation="en")
        transcript = loader.load()
        transcript = transcript[0]
        st.write(transcript.page_content)
    except Exception as e:
        transcript = 'test transcript'
        st.write('Error loading transcript')

if transcript:
    # Generate claims
    claims = generate_claims(transcript)
    claims = ''
    if claims:
        st.text_area("Generated claims from the input", claims, height=100)

    # Yes/No input and button
    yes_no = st.radio("Yes/No", ["Yes", "No"])
    if st.button("ent", key="yes_no_ent"):
        # Language Output
        st.text_input("Language Output", "Sample output based on Yes/No")

        # Generate offensive messaging sections
        for i in range(3):
            offensive_msg = generate_offensive_messaging(input_text)
            st.text_area(f"Generated offensive messaging from the input ({i+1})", offensive_msg, height=50)
else:
    st.warning("Please enter a video link.")

# Share button
if st.button("Share"):
    st.success("Sharing functionality would be implemented here")

