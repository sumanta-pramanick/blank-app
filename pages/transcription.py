import streamlit as st
import openai
import io
from navigation import make_sidebar

st.set_page_config(
    page_title="Audio and Video Transcription and Summarization",
    page_icon="👋",
)

make_sidebar()
openai.api_key = st.secrets["OPENAI_API_KEY"]


if "transcription" not in st.session_state:
    st.session_state.transcription = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "selected_language" not in st.session_state:
    st.session_state.selected_language = ""
if "translation" not in st.session_state:
    st.session_state.translation = ""


def transcribe(file):
    if file is not None:
        audio_buffer = io.BytesIO(file.getbuffer())
        audio_buffer.name = file.name
        response = openai.audio.transcriptions.create(
            model="whisper-1", file=audio_buffer
        )

        st.session_state.transcription = response.text


def summarize():
    summary_response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following text:\n\n{st.session_state.transcription}",
            }
        ],
        max_tokens=500,
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
        "Arabic": "ar",
    }

    target_language = language_codes.get(st.session_state.selected_language)

    translation_response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Translate the following text to {st.session_state.selected_language}:\n\n{st.session_state.summary}",
            }
        ],
    )
    st.session_state.translation = translation_response.choices[0].message.content


def click_reset():
    st.session_state.transcription = ""
    st.session_state.summary = ""
    st.session_state.selected_language = ""
    st.session_state.translation = ""


def main_page():
    style = """
        <style>
            button{
                float:right;
            }
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)
    st.title("Audio and Video Transcription")

    with st.container(border=True):
        file = st.file_uploader(
            "Upload Audio or Video File",
            type=["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"],
        )
        if file:
            if st.button("Transcribe"):
                transcribe(file)

    if st.session_state.transcription:
        with st.container(border=True):
            st.write("Transcription:")
            st.write(st.session_state.transcription)

            if st.button("Summarize Transcription"):
                summarize()

    if st.session_state.summary:
        with st.container(border=True):
            st.write("Summary:")
            st.write(st.session_state.summary)

            language = st.selectbox(
                "Select Language for Translation",
                [
                    "Hindi",
                    "Bengali",
                    "Telugu",
                    "Marathi",
                    "Gujarati",
                    "French",
                    "Spanish",
                    "Mandarin",
                    "Portuguese",
                    "Arabic",
                ],
            )
            st.session_state.selected_language = language

            if st.button("Translate Summary"):
                translate()

    if st.session_state.translation:
        with st.container(border=True):
            st.write(f"Translation in {st.session_state.selected_language}:")
            st.write(st.session_state.translation)
            st.write("")
            st.write("")
            st.button("Strat Over", on_click=click_reset)


main_page()
