# recorder.py
import logging
import threading
import time
import traceback
import wave
import numpy as np
import sounddevice as sd

import Tools.speechToText as speechToText
import Tools.VoiceModule.quickSearch as quickSearch


def _record_file(
    output_file="command.wav",
    stream=None,
    rate=16000,
    chunk_size=1280,
    device=None,
    status_callback=None,
    should_stop=None,
):
    """Records audio until silence or max duration and saves it to a WAV file."""
    MAX_DURATION = 7.0
    SILENCE_DURATION = 1.5
    SILENCE_THRESHOLD = 300

    max_chunks = int((rate * MAX_DURATION) / chunk_size)
    silence_chunks_limit = int((rate * SILENCE_DURATION) / chunk_size)

    frames = []
    silent_chunks = 0

    logging.info(f"[record_audio] Recording up to {MAX_DURATION}s (or {SILENCE_DURATION}s silence)...")

    def _capture_loop(active_stream):
        nonlocal silent_chunks
        for i in range(max_chunks):
            if should_stop and should_stop():
                return False

            if i % 12 == 0 and status_callback:
                seconds_left = max(1, int(MAX_DURATION - (i * chunk_size) / rate))
                status_callback(f"Speak now! Recording ({seconds_left}s)...")

            data, _ = active_stream.read(chunk_size)
            frames.append(bytes(data))

            audio_array = np.frombuffer(data, dtype=np.int16)
            rms = float(np.sqrt(np.mean(audio_array.astype(np.float32) ** 2)))

            if rms < SILENCE_THRESHOLD:
                silent_chunks += 1
            else:
                silent_chunks = 0

            if i > 6 and silent_chunks >= silence_chunks_limit:
                logging.info(f"[record_audio] Detected {SILENCE_DURATION}s of silence. Stopping early.")
                break
        return True

    try:
        if stream is not None:
            completed = _capture_loop(stream)
        else:
            with sd.RawInputStream(
                samplerate=rate,
                blocksize=chunk_size,
                dtype="int16",
                channels=1,
                device=device,
            ) as temp_stream:
                completed = _capture_loop(temp_stream)

        if not completed:
            return None

        raw_audio = b"".join(frames)

        with wave.open(output_file, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(rate)
            wf.writeframes(raw_audio)

        logging.info(f"[record_audio] Saved recording to '{output_file}' ({len(raw_audio)} bytes).")
        if status_callback:
            status_callback("Audio saved!")
        return output_file

    except Exception as e:
        logging.error(f"[record_audio] Unexpected error: {e}\n{traceback.format_exc()}")
        if status_callback:
            status_callback("Error saving audio.")
        time.sleep(1.5)
        return None


def _cookUnderstandProcess(worker, **kwargs):
    """Runs completely in the background: records first, then runs SpeechToText."""
    # 1. Record the file (waits here in the background until finished)
    saved_file = _record_file(**kwargs)

    # 2. check for text 
    text = speechToText.SpeechToText(saved_file)
    logging.info(f"Recognized text: '{text}'")

    # 3. use the small LLM with the text 
    output = quickSearch.run(text)
    print(output)

    # 4. use the big LLM if needed

    # 5. make a mp3 file of the output

    # 6. play the file


def start(**kwargs):
    """Starts _cookUnderstandProcess in the background and immediately returns."""
    worker = threading.Thread(daemon=True)
    worker.command = None  
    
    # Point the thread directly at _cookUnderstandProcess
    worker._target = _cookUnderstandProcess
    worker._args = (worker,)
    worker._kwargs = kwargs
    
    worker.start()
    return worker

def setVoiceCheckRequirements(intents: list[str]):
    """Modifies the intents checked during _cookUnderstandProcess."""
    global _voice_check_intents
    _voice_check_intents = list(intents)
    quickSearch.set_intents(_voice_check_intents)