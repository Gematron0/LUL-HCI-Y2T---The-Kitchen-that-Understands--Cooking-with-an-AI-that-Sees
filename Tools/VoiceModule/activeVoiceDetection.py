# activeVoiceDetection.py

import threading
import wave
import logging
import numpy as np

import Tools.speechToText as speechToText
import Tools.VoiceModule.quickSearch as quickSearch


# Audio configuration
SAMPLE_RATE = 16000
MAX_DURATION = 7.0
SILENCE_DURATION = 1.5
SILENCE_THRESHOLD = 300

OUTPUT_FILE = "command.wav"

# Recording state
_recording = False
_audio_buffer = []

_audio_lock = threading.Lock()
_processing_lock = threading.Lock()

_processing = False

_latest_result = []
_latest_input = []

# Preserve your existing public result names
LatestResult = _latest_result
LatestInput = _latest_input


def start():
    """
    Activates recording after the wake word is detected.
    Does NOT open another microphone.
    """

    global _recording, _audio_buffer

    with _audio_lock:

        if _recording or _processing:
            logging.info("Recording or processing already active.")
            return

        _audio_buffer = []
        _recording = True

    logging.info("Active voice recording started.")


def feed_audio(chunk):
    """
    Receives audio frames from passiveVoiceDetection.
    Audio format: 16 kHz, mono, int16.
    """

    global _recording
    global _audio_buffer
    global _processing

    audio = np.asarray(chunk, dtype=np.int16).reshape(-1)

    if len(audio) == 0:
        return

    should_finish = False
    saved_frames = None

    with _audio_lock:

        if not _recording:
            return

        _audio_buffer.append(audio.tobytes())

        total_samples = sum(len(frame) // 2 for frame in _audio_buffer)

        duration = total_samples / SAMPLE_RATE

        rms = float(np.sqrt(np.mean(audio.astype(np.float32) ** 2)))

        if rms < SILENCE_THRESHOLD:
            # Count silence in seconds using actual frame length.
            if not hasattr(feed_audio, "_silence_time"):
                feed_audio._silence_time = 0.0

            feed_audio._silence_time += len(audio) / SAMPLE_RATE

        else:
            feed_audio._silence_time = 0.0

        # Avoid stopping immediately before the user speaks.
        should_finish = duration >= MAX_DURATION or (
            duration >= 0.5 and feed_audio._silence_time >= SILENCE_DURATION
        )

        if should_finish:

            _recording = False
            _processing = True

            saved_frames = _audio_buffer.copy()
            _audio_buffer = []

            feed_audio._silence_time = 0.0

    if saved_frames is not None:

        threading.Thread(
            target=process_recording, args=(saved_frames,), daemon=True
        ).start()


def process_recording(frames):
    """
    Saves audio, runs speech recognition and quickSearch.
    """

    global _processing

    try:

        if not frames:
            return

        filename = OUTPUT_FILE

        raw_audio = b"".join(frames)

        with wave.open(filename, "wb") as wf:

            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)

            wf.writeframes(raw_audio)

        logging.info(f"Recording saved: {filename}")

        # Speech to text
        sentence = speechToText.SpeechToText(filename)

        if not sentence or not sentence.strip():

            logging.info("No speech recognized.")
            return

        logging.info(f"Recognized text: {sentence}")

        # Determine search type
        search_type = quickSearch.run(sentence)

        logging.info(f"Search type: {search_type}")

        # Extract information
        result = quickSearch.infoExtraction(search_type, sentence)

        logging.info(f"Extracted result: {result}")

        if result is not None:

            with _processing_lock:

                LatestResult.append(result)
                LatestInput.append(search_type)

    except Exception:

        logging.exception("Active voice processing failed.")

    finally:

        with _audio_lock:
            _processing = False

        logging.info("Active voice processing finished.")


def getNextResult():
    """
    Returns the next available result.
    """

    with _processing_lock:

        if not LatestResult:
            return None, None

        result = LatestResult.pop(0)
        input_type = LatestInput.pop(0)

        return result, input_type


def areThereResults():

    with _processing_lock:
        return len(LatestResult) > 0


def stop():

    global _recording, _audio_buffer

    with _audio_lock:

        _recording = False
        _audio_buffer = []

    logging.info("Active recording stopped.")
