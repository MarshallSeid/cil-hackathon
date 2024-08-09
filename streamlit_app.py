import streamlit as st
from openai import OpenAI
from constants import claim_prompt, counter_narrative_prompt
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
                {"role": "system", "content": claim_prompt},
                {"role": "user", "content": input_text}
            ],
            stream=False,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def generate_offensive_messaging(input_tex, language):
    # Placeholder function - replace with actual implementation
    if not client:
            st.error("Please enter your OpenAI API key to generate claims.")
            return None

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": counter_narrative_prompt + 'in ' + language},
                {"role": "user", "content": input_text}
            ],
            stream=False,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

st.title("AAPI Countering Disinformation")

# Input field and button
input_text = st.text_input("Input - ex: Youtube Link")
transcript = ''

if st.button('Load Transcript'): 
    try: 
        loader = YoutubeLoader.from_youtube_url(input_text, add_video_info=False,language=["en", "id","hi"],translation="en")
        transcript = loader.load()
        transcript = transcript[0]
        st.write(transcript)
    except Exception as e:
        st.write('Error loading transcript')
        st.write(transcript)

    # Generate claims
    claims = generate_claims(transcript)
    if claims:
        st.text_area("Generated claims from the input", claims, height=100)

# Yes/No input and button
yes_no = st.selectbox("Does this contain mis/disinformation?", ["No", "Yes"])

if yes_no == "Yes":
    language = st.selectbox(
        "Select output language",
        ["English", "Hindi", "Spanish", "Mandarin", "French", "Arabic"]
    )
    
    if st.button("Generate Offensive Messaging"):
        offensive_msg = generate_offensive_messaging(transcript, language)
        st.text_area(f"Generated counter/offensive messaging in {language}", offensive_msg, height=100)
    # Generate offensive messaging sections
    for i in range(3):
        offensive_msg = generate_offensive_messaging(transcript, "English")  # Default to English for these
        st.text_area(f"Generated offensive messaging from the input ({i+1})", offensive_msg, height=50)


# Share button
if st.button("Share"):
    st.success("Shared with the community! [Link to the community](https://sites.google.com/view/hindi-democracy-defenders/home?authuser=3)", icon="🔥")