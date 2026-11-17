from piper import PiperVoice
from piper.download_voices import download_voice
from pathlib import Path
import wave

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
        Voice.synthesize_wav(Text, WavFile)
    return AudioPath
