from piper import PiperVoice
from huggingface_hub import hf_hub_download
from pathlib import Path
import wave
import base64
import streamlit as st
import logging

Voice = None


@st.cache_resource
def _load_cached_voice() -> PiperVoice:
    voices_dir = Path("voices")
    voices_dir.mkdir(exist_ok=True)

    # Downloads directly from Hugging Face without needing manual URLs
    model_path = hf_hub_download(
        repo_id="rhasspy/piper-voices",
        filename="en/en_US/lessac/medium/en_US-lessac-medium.onnx",
        local_dir=voices_dir,
    )
    config_path = hf_hub_download(
        repo_id="rhasspy/piper-voices",
        filename="en/en_US/lessac/medium/en_US-lessac-medium.onnx.json",
        local_dir=voices_dir,
    )

    return PiperVoice.load(model_path, config_path=config_path)


def downlodeTextToSpeechModel() -> None:
    global Voice
    Voice = _load_cached_voice()


def TextToSpeech(Text: str, AudioPath: str = "speech.wav") -> str:
    if Voice is None:
        downlodeTextToSpeechModel()
    with wave.open(AudioPath, "wb") as WavFile:
        WavFile.setnchannels(1)
        WavFile.setsampwidth(2)
        WavFile.setframerate(Voice.config.sample_rate)
        Voice.synthesize_wav(Text, WavFile, set_wav_format=False)
    return AudioPath


def PlayAudio(file_path: str = "speech.wav", mime_type: str = "audio/wav") -> None:
    logging.info(f"attempting to play audio: {file_path}")
    with open(file_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        html = f"""
        <audio autoplay style="display:none;">
            <source src="data:{mime_type};base64,{b64}" type="{mime_type}">
        </audio>
        """
    st.markdown(html, unsafe_allow_html=True)