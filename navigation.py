import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(
                "https://awsmp-logos.s3.amazonaws.com/0ba0cfff-f9da-474c-9aea-7ce69f505034/9c50547121ad1016ef9c6e9ef9804cdc.png"
            )
            st.write("")
            st.write("")

        if st.session_state.get("logged_in") == True:
            st.write("")
            st.sidebar.title("Transcribe Menu")
            st.page_link(
                "pages/plagiarism.py",
                label="Plagiarism Detection",
                icon=":material/plagiarism:",
            )
            st.page_link(
                "pages/transcription.py",
                label="Transcription",
                icon=":material/transcribe:",
            )

            st.write("")
            st.sidebar.title("")
            st.sidebar.write("")

            if st.button("Log out"):
                logout()

        elif get_current_page_name() != "login":
            st.switch_page("login.py")


def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("login.py")
