import streamlit as st
import random
import time

def start(app_ui):
    placeholder = app_ui.empty()
    
    with placeholder.container(height=600, border=False):
        st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
        
        st.markdown(
            "<h1 style='text-align: center;'>Welcome to the cookbook app</h1>", 
            unsafe_allow_html=True
        )
        
        # Center the progress bar using columns so it doesn't stretch across the whole screen
        st.markdown(
            """
            <style>
            div[data-testid="stProgress"] {
                margin-bottom: -24px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            master_progress_bar = st.progress(0, text="Please wait while we complete some final checks")
            minor_progress_bar = st.progress(0, text="")

            
        st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
        
        fun_facts = [
            "This project contains many different AIs",
            "This was only coded in 10 weeks",
            "idk something"
        ]
        fun_fact = random.choice(fun_facts)
        st.markdown(
            f"<p style='text-align: center; color: gray;'>Fun fact: {fun_fact}</p>", 
            unsafe_allow_html=True
        )

    # Return both the placeholder and the progress_bar so you can update it
    return placeholder, master_progress_bar, minor_progress_bar

def stop(placeholder):
    placeholder.empty()