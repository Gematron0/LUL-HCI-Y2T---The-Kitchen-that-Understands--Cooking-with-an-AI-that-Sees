from piper import PiperVoice
from piper.download_voices import download_voice
from pathlib import Path
import wave
import base64
import streamlit as st
import logging


Voice = None


def downlodeTextToSpeechModel() -> None:
    global Voice
    Path("voices").mkdir(exist_ok=True)
    download_voice("en_US-lessac-medium", Path("voices"))
    Voice = PiperVoice.load("voices/en_US-lessac-medium.onnx")


def TextToSpeech(Text, AudioPath="speech.wav") -> str:
    if Voice is None:
        downlodeTextToSpeechModel()
    with wave.open(AudioPath, "wb") as WavFile:
        WavFile.setnchannels(1)
        WavFile.setsampwidth(2)
        WavFile.setframerate(Voice.config.sample_rate)
        Voice.synthesize_wav(Text, WavFile, set_wav_format=False)
    return AudioPath


def PlayAudio(file_path: str = "speech.wav", mime_type: str = "audio/wav"):
    logging.info(f"attempting to play audio: {file_path}")
    with open(file_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        html = f"""
        <audio autoplay style="display:none;">
            <source src="data:{mime_type};base64,{b64}" type="{mime_type}">
        </audio>
        """
    st.markdown(html, unsafe_allow_html=True)
