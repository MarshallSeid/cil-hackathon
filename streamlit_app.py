import streamlit as st
# from openai import OpenAI

# Initialize OpenAI client
client = None

def initialize_openai_client():
    global client
    api_key = st.session_state.get('openai_api_key')
    if api_key:
        client = OpenAI(api_key=api_key)

def generate_claims(input_text):
    if not client:
        st.error("Please enter your OpenAI API key to generate claims.")
        return None
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "cont`ent": "Analyze the following text and identify the main claims:"},
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

# API Key input
api_key = st.text_input("OpenAI API Key", type="password")
if api_key:
    st.session_state['openai_api_key'] = api_key
    initialize_openai_client()

# Input field and button
input_text = st.text_input("Input - ex: Youtube Link")

if st.button("ent", key="input_ent"):
    if input_text:
        # Generate claims
        claims = generate_claims(input_text)
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
        st.warning("Please enter some input text.")

# Share button
if st.button("Share"):
    st.success("Sharing functionality would be implemented here")

