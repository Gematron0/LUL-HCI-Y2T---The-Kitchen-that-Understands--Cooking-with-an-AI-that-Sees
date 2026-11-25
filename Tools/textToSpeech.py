from piper import PiperVoice
from pathlib import Path
import urllib.request
import wave
import base64
import streamlit as st
import logging

Voice = None


@st.cache_resource
def _load_cached_voice() -> PiperVoice:
    voices_dir = Path("voices")
    voices_dir.mkdir(exist_ok=True)

    model_path = voices_dir / "en_US-lessac-medium.onnx"
    config_path = voices_dir / "en_US-lessac-medium.onnx.json"

    # Remove empty or corrupted files from previous failed downloads
    if config_path.exists() and config_path.stat().st_size == 0:
        config_path.unlink()
    if model_path.exists() and model_path.stat().st_size == 0:
        model_path.unlink()

    # Full path to the voice model on Hugging Face
    base_url = (
        "https://huggingface.co"
        "en/en_US/lessac/medium"
    )
    if not model_path.exists():
        logging.info("Downloading Piper ONNX model...")
        urllib.request.urlretrieve(f"{base_url}/en_US-lessac-medium.onnx", model_path)
    if not config_path.exists():
        logging.info("Downloading Piper JSON config...")
        urllib.request.urlretrieve(f"{base_url}/en_US-lessac-medium.onnx.json", config_path)

    return PiperVoice.load(str(model_path), config_path=str(config_path))


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