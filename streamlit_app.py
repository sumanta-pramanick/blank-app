import streamlit as st
import openai
from moviepy.editor import VideoFileClip
import os
from pydub import AudioSegment
import io

st.set_page_config(
    page_title="Audio and Video Transcription and Summarization",
    page_icon="👋",
)

openai.api_key = st.secrets["OPENAI_API_KEY"]


if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'transcription' not in st.session_state:
    st.session_state.transcription = ''
if 'summary' not in st.session_state:
    st.session_state.summary = ''
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = ''
if 'translation' not in st.session_state:
    st.session_state.translation = ''

def transcribe(file):
    if file is not None:
        audio_buffer = io.BytesIO(file.getbuffer())
        audio_buffer.name = file.name
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_buffer
        )

        st.session_state.transcription = response.text
        

def summarize():
    summary_response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Summarize the following text:\n\n{st.session_state.transcription}"}],
        max_tokens=500
    )
    st.session_state.summary = summary_response.choices[0].message.content

def translate():
    language_codes = {
        "Hindi": "hi",
        "Bengali": "bn",
        "Telugu": "te",
        "Marathi": "mr",
        "Gujarati": "gu",
        "French": "fr",
        "Spanish": "es",
        "Mandarin": "zh",
        "Portuguese": "pt",
        "Arabic": "ar"
    }

    target_language = language_codes.get(st.session_state.selected_language)

    translation_response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Translate the following text to {st.session_state.selected_language}:\n\n{st.session_state.summary}"}],
        max_tokens=150
    )
    st.session_state.translation = translation_response.choices[0].message.content

user_id = None
password = None

def click_login():   
    uid = st.secrets["user_id"]
    pwd = st.secrets["password"]
    if user_id == uid and password == pwd:
        st.session_state.logged_in = True
    else:
        st.error("Invalid login credentials")

def click_reset():
    st.session_state.logged_in = True
    st.session_state.transcription = ''
    st.session_state.summary = ''
    st.session_state.selected_language = ''
    st.session_state.translation = ''

def main_page():
    st.markdown("""
        <div style="border:2px solid #4CAF50; padding: 10px; border-radius: 10px; text-align: center;">
            <h1 style="color: black;font-size: 24px">Audio and Video Transcription and Summarization</h1>
        </div>
        """, unsafe_allow_html=True)

    file = st.file_uploader("Upload Audio or Video File", type=["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"])
    if file:
        if st.button("Transcribe"):
            transcribe(file)

    if st.session_state.transcription:
        st.write("Transcription:")
        st.write(st.session_state.transcription)

        if st.button("Summarize Transcription"):
            summarize()

    if st.session_state.summary:
        st.write("Summary:")
        st.write(st.session_state.summary)

        language = st.selectbox(
            "Select Language for Translation",
            ["Hindi", "Bengali", "Telugu", "Marathi", "Gujarati", "French", "Spanish", "Mandarin", "Portuguese", "Arabic"]
        )
        st.session_state.selected_language = language

        if st.button("Translate Summary"):
            translate()

    if st.session_state.translation:
        st.write(f"Translation in {st.session_state.selected_language}:")
        st.write(st.session_state.translation)
        st.write("")
        st.write("")
        st.button("Strat Over", on_click=click_reset)


col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://awsmp-logos.s3.amazonaws.com/0ba0cfff-f9da-474c-9aea-7ce69f505034/9c50547121ad1016ef9c6e9ef9804cdc.png")



if not st.session_state.logged_in:
    st.title("Login")
    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")
    st.button("Login", on_click=click_login)
        # login(user_id, password, placeholder)
else:
    main_page()