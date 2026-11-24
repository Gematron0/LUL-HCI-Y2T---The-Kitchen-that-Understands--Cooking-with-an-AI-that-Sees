import streamlit as st
import time

if "step" not in st.session_state:
    st.session_state.step = 1

def go_to_page2():
    time.sleep(2)
    st.session_state.step = 2
    st.rerun()

def back_button():
    st.session_state.step -=1
    st.rerun()


if st.session_state.step == 1:
    st.title("Voice Assistant AI Cooker")
    st.header("Your personal AI Voice Assistant Cooker")

    with st.spinner("Initializing your AI cooker..."):
        go_to_page2()


elif st.session_state.step == 2:
    st.header("This is page 1")
