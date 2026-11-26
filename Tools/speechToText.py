# this file contains AI

from faster_whisper import WhisperModel
import logging
import time

Model = None
import streamlit as st

@st.cache_resource(show_spinner=False)
def downlodeSpeechToTextModel() -> None:
    global Model
    Start = time.time()
    logging.info(f"Downloading speech to text model")
    Model = WhisperModel("base")
    logging.info(f"DownLode compleat; time: {time.time()-Start}")
    return


def SpeechToText(AudioPath) -> str:
    logging.info(f"Started speech to text")
    StartTime = time.time()

    if not isinstance(AudioPath, str):
        logging.error(f"AudioPath must be a str; got: {type(AudioPath)}")
        raise ValueError("AudioPath must be an str.")

    if Model is None:
        downlodeSpeechToTextModel()

    Segments, Info = Model.transcribe(AudioPath)

    Text = ""
    for Segment in Segments:
        Text += Segment.text

    Text = Text.strip()
    logging.info(f"Completed, time: {time.time()-StartTime}")
    logging.info(f"Text: {Text}")
    return Text
