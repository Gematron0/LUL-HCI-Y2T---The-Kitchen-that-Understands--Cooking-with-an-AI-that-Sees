# this file contains generative AI

import logging
import os
import threading
import time
import traceback
import wave
import numpy as np
import sounddevice as sd
import streamlit as st
from openwakeword.model import Model


class _VoiceWorker:
    def __init__(self, model_path="hey_cookbook.onnx", device=None, output_file="command.wav"):
        self.model_path = model_path
        self.wake_word = os.path.splitext(os.path.basename(model_path))[0]
        self.device = device
        self.output_file = output_file

        self.status = f"Initializing '{self.wake_word.replace('_', ' ')}'..."
        self.has_new_audio = False  # Flag to let main.py know a new recording is ready
        self.running = False
        self.lock = threading.Lock()
        logging.info(f"[_VoiceWorker.__init__] Initialized with model='{self.model_path}'")

    def start(self):
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self._listen_loop, name="VoiceListenerThread", daemon=True)
            thread.start()
            logging.info(f"[_VoiceWorker.start] Started background thread: {thread.name}")

    def _listen_loop(self):
        logging.info("[_listen_loop] Entered background listener thread.")
        try:
            RATE = 16000
            CHUNK = 1280  # 80ms per chunk

            oww_model = Model(wakeword_model_paths=[self.model_path])
            logging.info(f"[_listen_loop] Active models: {list(oww_model.models.keys())}")

            with self.lock:
                self.status = f"Listening for '{self.wake_word.replace('_', ' ')}'..."

            chunk_counter = 0
            max_score_seen = 0.0

            while self.running:
                try:
                    with sd.RawInputStream(
                        samplerate=RATE,
                        blocksize=CHUNK,
                        dtype="int16",
                        channels=1,
                        device=self.device
                    ) as stream:
                        while self.running:
                            data, overflowed = stream.read(CHUNK)
                            audio_array = np.frombuffer(data, dtype=np.int16)
                            prediction = oww_model.predict(audio_array)
                            score = max(
                                (v for k, v in prediction.items() if k.startswith(self.wake_word)),
                                default=0.0
                            )

                            if score > max_score_seen:
                                max_score_seen = score

                            chunk_counter += 1
                            if chunk_counter % 62 == 0:
                                rms = float(np.sqrt(np.mean(audio_array.astype(np.float32) ** 2)))
                                logging.info(
                                    f"Heartbeat | mic_rms={rms:.1f} | max_score_last_5s={max_score_seen:.4f}"
                                )
                                max_score_seen = 0.0

                            if score > 0.5:
                                logging.info(f">>> WAKE WORD TRIGGERED (score={score:.4f}) <<<")
                                self._record_audio(stream, RATE, CHUNK)
                                oww_model.reset()
                                max_score_seen = 0.0
                                with self.lock:
                                    self.status = f"Listening for '{self.wake_word.replace('_', ' ')}'..."

                except Exception as loop_err:
                    logging.warning(f"Inner loop exception: {loop_err}\n{traceback.format_exc()}")
                    with self.lock:
                        self.status = f"Audio error: {loop_err}"
                    time.sleep(1.0)

        except Exception as fatal_err:
            logging.error(f"FATAL thread crash: {fatal_err}\n{traceback.format_exc()}")
            with self.lock:
                self.status = f"Fatal voice error: {fatal_err}"

    def _record_audio(self, stream, rate, chunk_size):
        MAX_DURATION = 7.0       # Maximum seconds to record
        SILENCE_DURATION = 1.5   # Stop after 1,5 second of silence
        SILENCE_THRESHOLD = 300  # Adjust based on your mic_rms heartbeat in the logs

        max_chunks = int((rate * MAX_DURATION) / chunk_size)               # ~62 chunks (5.0s)
        silence_chunks_limit = int((rate * SILENCE_DURATION) / chunk_size) # ~12 chunks (1.0s)

        frames = []
        silent_chunks = 0

        logging.info(f"Recording up to {MAX_DURATION}s (or {SILENCE_DURATION}s silence)...")

        try:
            for i in range(max_chunks):
                if not self.running:
                    return

                if i % 12 == 0:
                    seconds_left = max(1, int(MAX_DURATION - (i * chunk_size) / rate))
                    with self.lock:
                        self.status = f"Speak now! Recording ({seconds_left}s)..."

                data, _ = stream.read(chunk_size)
                frames.append(bytes(data))

                # Calculate volume (RMS) of the current chunk
                audio_array = np.frombuffer(data, dtype=np.int16)
                rms = float(np.sqrt(np.mean(audio_array.astype(np.float32) ** 2)))

                if rms < SILENCE_THRESHOLD:
                    silent_chunks += 1
                else:
                    silent_chunks = 0

                # Stop early if quiet for 1 second (skip checking during the first 0.5s)
                if i > 6 and silent_chunks >= silence_chunks_limit:
                    logging.info(f"[_record_audio] Detected {SILENCE_DURATION}s of silence. Stopping early.")
                    break

            raw_audio = b"".join(frames)

            # Always overwrite the same file
            with wave.open(self.output_file, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)  # 2 bytes = 16-bit audio
                wf.setframerate(rate)
                wf.writeframes(raw_audio)

            logging.info(f"[_record_audio] Saved recording to '{self.output_file}' ({len(raw_audio)} bytes).")

            with self.lock:
                self.has_new_audio = True
                self.status = "Audio saved!"

        except Exception as e:
            logging.info(f"[_record_audio] Unexpected error: {e}\n{traceback.format_exc()}")
            with self.lock:
                self.status = "Error saving audio."
            time.sleep(1.5)

    @staticmethod
    def find_input_device(name_substring: str):
        """Finds the first input device index matching the given name substring."""
        if not name_substring:
            return None  # Falls back to system default

        for idx, dev in enumerate(sd.query_devices()):
            if dev["max_input_channels"] > 0 and name_substring.lower() in dev["name"].lower():
                logging.info(f"Matched audio device [{idx}]: {dev['name']}")
                return idx

        logging.warning(f"Device '{name_substring}' not found. Falling back to system default.")
        return None


@st.cache_resource
def _get_worker():
    logging.info("[_get_worker] Creating cached _VoiceWorker singleton...")
    worker = _VoiceWorker(model_path="hey_cookbook.onnx", device=None, output_file="command.wav")
    worker.start()
    return worker


def start(ui_container=None):
    """Call this from main.py to start passive listening silently in the background."""
    _get_worker()


def get_latest_audio_file():
    """Returns 'command.wav' once when a new recording finishes, otherwise returns empty string."""
    worker = _get_worker()
    with worker.lock:
        if worker.has_new_audio:
            worker.has_new_audio = False
            return worker.output_file
    return ""