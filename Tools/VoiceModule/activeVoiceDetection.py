
# activeVoiceDetection.py

import threading
import wave
import logging
import os
import uuid

import numpy as np

import Tools.speechToText as speechToText
import Tools.VoiceModule.quickSearch as quickSearch


# ============================================================
# AUDIO CONFIGURATION
# ============================================================

SAMPLE_RATE = 16000
CHANNELS = 1
SAMPLE_WIDTH = 2

MAX_DURATION = 7.0
SILENCE_DURATION = 1.5
SILENCE_THRESHOLD = 300

OUTPUT_DIR = "recordings"


# ============================================================
# RECORDING STATE
# ============================================================

_recording = False
_processing = False

_audio_buffer = []
_silence_time = 0.0

_audio_lock = threading.Lock()
_processing_lock = threading.Lock()

_latest_result = []
_latest_input = []

# Preserve existing public result names
LatestResult = _latest_result
LatestInput = _latest_input


# ============================================================
# START ACTIVE RECORDING
# ============================================================

def start():

    global _recording
    global _audio_buffer
    global _silence_time

    with _audio_lock:

        if _recording or _processing:
            logging.info(
                "Recording or processing already active."
            )
            return

        _audio_buffer = []
        _silence_time = 0.0

        _recording = True

    logging.info("Active voice recording started.")


# ============================================================
# RECEIVE AUDIO FROM WEBRTC
# ============================================================

def feed_audio(chunk):

    global _recording
    global _processing
    global _audio_buffer
    global _silence_time

    if chunk is None:
        return

    audio = np.asarray(
        chunk,
        dtype=np.int16
    ).reshape(-1)

    if len(audio) == 0:
        return

    saved_frames = None

    with _audio_lock:

        if not _recording:
            return

        # Store the exact audio received from WebRTC.
        _audio_buffer.append(audio.copy())

        # Calculate current recording duration.
        total_samples = sum(
            len(frame) for frame in _audio_buffer
        )

        duration = total_samples / SAMPLE_RATE

        # Calculate RMS volume.
        rms = float(
            np.sqrt(
                np.mean(
                    audio.astype(np.float32) ** 2
                )
            )
        )

        # Detect silence.
        if rms < SILENCE_THRESHOLD:

            _silence_time += len(audio) / SAMPLE_RATE

        else:

            _silence_time = 0.0

        # Decide when to finish recording.
        should_finish = (
            duration >= MAX_DURATION
            or (
                duration >= 0.5
                and _silence_time >= SILENCE_DURATION
            )
        )

        if should_finish:

            _recording = False
            _processing = True

            saved_frames = _audio_buffer.copy()

            _audio_buffer = []
            _silence_time = 0.0

            logging.info(
                f"Recording finished. "
                f"Duration={duration:.2f}s"
            )

    # Process outside the audio lock.
    if saved_frames is not None:

        threading.Thread(
            target=process_recording,
            args=(saved_frames,),
            daemon=True
        ).start()


# ============================================================
# SAVE AUDIO AS WAV
# ============================================================

def save_audio(frames):

    if not frames:
        raise ValueError("No audio frames received.")

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    filename = os.path.join(
        OUTPUT_DIR,
        f"command_{uuid.uuid4().hex}.wav"
    )

    raw_audio = np.concatenate(frames).astype(
        np.int16,
        copy=False
    )

    with wave.open(filename, "wb") as wf:

        wf.setnchannels(CHANNELS)
        wf.setsampwidth(SAMPLE_WIDTH)
        wf.setframerate(SAMPLE_RATE)

        wf.writeframes(raw_audio.tobytes())

    if not os.path.isfile(filename):
        raise IOError("WAV file was not created.")

    if os.path.getsize(filename) <= 44:
        raise IOError("WAV file contains no audio data.")

    logging.info(
        f"Recording saved: {filename}"
    )

    return filename


# ============================================================
# PROCESS RECORDING
# ============================================================

def process_recording(frames):

    global _processing

    filename = None

    try:

        if not frames:
            logging.warning("Empty recording received.")
            return

        # Save the audio.
        filename = save_audio(frames)

        # Verify the filename before speech recognition.
        if not isinstance(filename, str):
            raise ValueError(
                "Invalid audio filename."
            )

        if not os.path.exists(filename):
            raise FileNotFoundError(filename)

        # ----------------------------------------------------
        # SPEECH TO TEXT
        # ----------------------------------------------------

        logging.info("Starting speech recognition.")

        sentence = speechToText.SpeechToText(
            filename
        )

        if not sentence or not sentence.strip():

            logging.info("No speech recognized.")
            return

        logging.info(
            f"Recognized text: {sentence}"
        )

        # ----------------------------------------------------
        # QUICK SEARCH
        # ----------------------------------------------------

        search_type = quickSearch.run(
            sentence
        )

        logging.info(
            f"Search type: {search_type}"
        )

        # ----------------------------------------------------
        # INFORMATION EXTRACTION
        # ----------------------------------------------------

        result = quickSearch.infoExtraction(
            search_type,
            sentence
        )

        logging.info(
            f"Extracted result: {result}"
        )

        if result is not None:

            with _processing_lock:

                LatestResult.append(result)
                LatestInput.append(search_type)

    except Exception:

        logging.exception(
            "Active voice processing failed."
        )

    finally:

        # Clean up temporary recording.
        if filename and os.path.exists(filename):

            try:
                os.remove(filename)

            except OSError:

                logging.warning(
                    f"Could not remove temporary file: {filename}"
                )

        with _audio_lock:

            _processing = False

        logging.info(
            "Active voice processing finished."
        )


# ============================================================
# GET RESULTS
# ============================================================

def getNextResult():

    with _processing_lock:

        if not LatestResult:
            return None, None

        result = LatestResult.pop(0)
        input_type = LatestInput.pop(0)

        return result, input_type


def areThereResults():

    with _processing_lock:

        return len(LatestResult) > 0


# ============================================================
# STOP ACTIVE RECORDING
# ============================================================

def stop():

    global _recording
    global _audio_buffer
    global _silence_time

    with _audio_lock:

        _recording = False
        _audio_buffer = []
        _silence_time = 0.0

    logging.info(
        "Active recording stopped."
    )