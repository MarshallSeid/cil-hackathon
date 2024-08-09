import streamlit as st
from openai import OpenAI
from constants import claim_prompt, counter_narrative_prompt
# langchain 
from langchain_community.document_loaders import YoutubeLoader
from youtube_content_engine import search_videos, fetch_high_polarity_video

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

st.title("Top polarizing content for candidate")
query = st.text_input("Refine:", value='filter polarizing content')
language = st.selectbox("Select language:", [('Hindi', 'hi'), ('Mandarin', 'zh-CN'), ('Cantonese', 'zh-TW')], index=0)

results = fetch_high_polarity_video()
if results:
    cols = st.columns(3)  # Create 3 columns
    index = 0
    for query, video_stats in results.items():
        for video_stat in video_stats:
            video = video_stat.get('video')
            stats = video_stat.get('stats')
            with cols[index % 3]:  # This will distribute videos across the 3 columns
                st.image(f"https://img.youtube.com/vi/{video_stat.get('video').get('id')}/0.jpg", use_column_width=True)
                st.subheader(video['title'])
                st.write(f"Channel: {video['channel_title']}")
                st.write(f"Published: {video['published_at']}")
                
                if stats:
                    st.write(f"Views: {stats.get('viewCount', 'N/A')}")
                    st.write(f"Likes: {stats.get('likeCount', 'N/A')}")
                
                st.markdown(f"https://www.youtube.com/watch?v={video['id']}")
                st.write("---")
                index += 1
else:
    st.warning("No videos found matching the criteria.")

# Input field and button
input_text = st.text_input("Input - ex: Youtube Link")
transcript = ''

if st.button('Load Transcript'): 
    try: 
        loader = YoutubeLoader.from_youtube_url(input_text, add_video_info=False,language=["en", "id","hi"],translation="en")
        transcript = loader.load()
        transcript = transcript[0]
    except Exception as e:
        transcript = 'test transcript'
        st.write('Error loading transcript')

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