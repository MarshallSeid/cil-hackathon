import streamlit as st
from openai import OpenAI
from constants import claim_prompt, counter_narrative_prompt
# langchain 
from langchain_community.document_loaders import YoutubeLoader
import pandas as pd

# Sample data for CSV
data = {
    'Column1': [1, 2, 3],
    'Column2': ['A', 'B', 'C']
}
df = pd.DataFrame(data)

# Initialize OpenAI client
client = None

def initialize_openai_client():
    global client
    api_key = st.secrets["OPENAI_TOKEN"]
    if api_key:
        client = OpenAI(api_key=api_key)

# API Key input
initialize_openai_client()


st.markdown("""
    <style>
    .blue-button {
        background-color: #007BFF;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)


def generate_claims(input_text):
    input_text = input_text.page_content
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
    except Exception as e:
        st.write('Error loading transcript' + str(e))

if transcript:
    # Generate claims
    claims = generate_claims(transcript)
    if claims:
        st.text_area("Generated claims from the input", claims, height=400)

    # Yes/No input and button
    yes_no = st.selectbox("Does this contain mis/disinformation?", ["Yes", "No"])    

    if yes_no == "Yes":
        language = st.selectbox(
            "Select output language",
            ["English", "Hindi", "Spanish", "Mandarin", "French", "Arabic"]
        )

        # HTML for the button
        if st.markdown('<button class="blue-button">Generate counter narrative Messaging</button>', unsafe_allow_html=True):
            offensive_msg = generate_offensive_messaging(transcript, language)
            st.text_area(f"Generated positive/counter narrative messaging in {language}", offensive_msg, height=100)
    
    # Generate offensive messaging sections
    for i in range(3):
        offensive_msg = generate_offensive_messaging(transcript, "English")  # Default to English for these
        st.text_area(f"Generated positive/counter narrative messaging from the input - {i+1}", offensive_msg, height=500)
else:
    st.warning("Please enter a video link.")

# Share button
if st.button("Share"):
    st.success("Shared with the community! [Link to the community](https://sites.google.com/view/hindi-democracy-defenders/home?authuser=3)", icon="🔥")

# Export button
st.download_button(
    label="Export CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name='PotentialDisinformationBreakdown.csv',
    mime='text/csv')