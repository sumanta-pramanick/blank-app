import streamlit as st
import openai
from moviepy.editor import VideoFileClip
import os
from pydub import AudioSegment

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

def login(user_id, password):
    if user_id == "Kellton" and password == "Kellton@404":
        st.session_state.logged_in = True
    else:
        st.error("Invalid login credentials")

# Transcription functions
def transcribe():
    if file is not None:
        file_extension = file.name.split('.')[-1]

        if file_extension in ["mp4", "avi", "mov", "mkv"]:
            with open("uploaded_video." + file_extension, "wb") as f:
                f.write(file.getbuffer())

            video_clip = VideoFileClip("uploaded_video." + file_extension)
            audio_path = "extracted_audio.wav"
            video_clip.audio.write_audiofile(audio_path)
            video_clip.close()
            os.remove("uploaded_video." + file_extension)
        elif file_extension in ["mp3", "wav"]:
            with open("uploaded_audio." + file_extension, "wb") as f:
                f.write(file.getbuffer())

            if file_extension == "mp3":
                audio = AudioSegment.from_mp3("uploaded_audio.mp3")
                audio.export("uploaded_audio.wav", format="wav")
                audio_path = "uploaded_audio.wav"
                os.remove("uploaded_audio.mp3")
            else:
                audio_path = "uploaded_audio.wav"

        with open(audio_path, "rb") as audio_file:
            response = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        st.session_state.transcription = response
        os.remove(audio_path)

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


if not st.session_state.logged_in:
    logo_path = "https://awsmp-logos.s3.amazonaws.com/0ba0cfff-f9da-474c-9aea-7ce69f505034/9c50547121ad1016ef9c6e9ef9804cdc.png"
    col1, col2, col3= st.columns([1,2,1])
    with col2:
        st.image(logo_path,use_column_width=True)
        
    st.title("Login")
    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        login(user_id, password)
else:
    logo_path = "https://awsmp-logos.s3.amazonaws.com/0ba0cfff-f9da-474c-9aea-7ce69f505034/9c50547121ad1016ef9c6e9ef9804cdc.png"
    col1, col2, col3= st.columns([1,2,1])
    with col2:
        st.image(logo_path,use_column_width=True)
         
    st.markdown("""
        <div style="border:2px solid #4CAF50; padding: 10px; border-radius: 10px; text-align: center;">
            <h1 style="color: black;font-size: 24px">Audio and Video Transcription and Summarization</h1>
        </div>
        """, unsafe_allow_html=True)

    file = st.file_uploader("Upload Audio or Video File", type=["mp3", "wav", "mp4", "avi", "mov", "mkv"])

    if file:
        if st.button("Transcribe"):
            transcribe()

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
