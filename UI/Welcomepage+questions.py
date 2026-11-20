import streamlit as st
import time

if "step" not in st.session_state:
    st.session_state.step = 1

if "info" not in st.session_state:
    st.session_state.info={}

def next_page():
    st.session_state.step+=1
    time.sleep(2)
    st.rerun()

def back_button():
    if st.session_state.step>1:
     st.session_state.step-=1
     st.rerun()
    else:
        st.write("Can't go any further")


if st.session_state.step == 1:
    st.title("Voice Assistant AI Cooker")
    st.header("Your personal AI Voice Assistant Cooker")

    with st.spinner("Initializing your AI cooker..."):
        next_page()


elif st.session_state.step == 2:
    st.header("Before we start we would like as some questions")
    with st.form(key="User_info_form"):
     name= st.text_input("Please enter your name (No need for real one)", value=st.session_state.info.get("name",""))
     allergies = st.multiselect("Do you have any allergies?",options=["Peanuts", "Milk", "Eggs", "Gluten", "Soy"], default=st.session_state.info.get("allergies", []))
     if st.form_submit_button():
        next_page()

elif st.session_state.step ==3:
    st.write("Page2")
    if st.button("Back"):
        back_button()
