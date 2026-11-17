from piper import PiperVoice
from piper.download_voices import download_voice
from pathlib import Path
import logging
import time
import wave

VoiceName = "en_US-lessac-medium"
VoiceFolder = Path("voices")
Voice = None

def downlodeTextToSpeechModel() -> None:
    global Voice
    Start = time.time()
    logging.info(f"Downloading text to speech voice: {VoiceName}")
    VoiceFolder.mkdir(exist_ok=True)
    download_voice(VoiceName, VoiceFolder)
    Voice = PiperVoice.load(VoiceFolder / f"{VoiceName}.onnx")
    logging.info(f"DownLode compleat; time: {time.time()-Start}")
    return

def TextToSpeech(Text, AudioPath="speech.wav") -> str:
    logging.info(f"Started text to speech")
    StartTime = time.time()

    if not isinstance(Text, str) or Text.strip() == "":
        logging.error(f"Text must be a str that is not empty; got: {Text!r}")
        raise ValueError("Text must be an str that is not empty.")

    if Voice is None:
        downlodeTextToSpeechModel()

    with wave.open(AudioPath, "wb") as WavFile:
        Voice.synthesize_wav(Text, WavFile)

    logging.info(f"Completed, time: {time.time()-StartTime}")
    logging.info(f"Audio saved to: {AudioPath}")
    return AudioPath
