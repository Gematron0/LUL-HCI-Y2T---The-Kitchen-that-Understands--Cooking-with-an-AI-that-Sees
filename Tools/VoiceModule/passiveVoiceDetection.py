# this file contains generative AI

import logging
import os
import threading
import time
import traceback
import numpy as np
import sounddevice as sd
import streamlit as st
from openwakeword.model import Model

import Tools.VoiceModule.activeVoiceDetection as activeVoiceDetection


class _VoiceWorker:
    def __init__(
        self, model_path="hey_cookbook.onnx", device=None, output_file="command.wav"
    ):
        self.model_path = model_path
        self.wake_word = os.path.splitext(os.path.basename(model_path))[0]
        self.device = device
        self.output_file = output_file

        self.status = f"Initializing '{self.wake_word.replace('_', ' ')}'..."
        self.has_new_audio = False  # Flag to let main.py know a new recording is ready
        self.running = False
        self.thread = None
        self.lock = threading.Lock()
        logging.debug(f"initialized with model='{self.model_path}'")

    def start(self):
        with self.lock:
            if not self.running:
                self.running = True
                self.thread = threading.Thread(
                    target=self._listen_loop, name="VoiceListenerThread", daemon=True
                )
                self.thread.start()
                logging.debug(f"Started background thread: {self.thread.name}")

    def stop(self):
        """Stops the audio stream and terminates the background listener thread."""
        with self.lock:
            if not self.running:
                return
            self.running = False
            thread_to_join = self.thread

        # Wait briefly outside the lock for the audio stream to finish its current 80ms chunk and close
        if (
            thread_to_join
            and thread_to_join.is_alive()
            and threading.current_thread() != thread_to_join
        ):
            thread_to_join.join(timeout=1.0)

        self._update_status("Voice detection stopped.")
        logging.info("Stopped passive wake-word listening.")

    def _update_status(self, message: str):
        with self.lock:
            self.status = message

    def _listen_loop(self):
        logging.debug("Entered background listener thread.")
        try:
            RATE = 16000
            CHUNK = 1280  # 80ms per chunk

            oww_model = Model(wakeword_model_paths=[self.model_path])
            logging.debug(f"Active models: {list(oww_model.models.keys())}")

            self._update_status(
                f"Listening for '{self.wake_word.replace('_', ' ')}'..."
            )

            chunk_counter = 0
            max_score_seen = 0.0

            while self.running:
                try:
                    with sd.RawInputStream(
                        samplerate=RATE,
                        blocksize=CHUNK,
                        dtype="int16",
                        channels=1,
                        device=self.device,
                    ) as stream:
                        while self.running:
                            data, overflowed = stream.read(CHUNK)
                            audio_array = np.frombuffer(data, dtype=np.int16)
                            prediction = oww_model.predict(audio_array)
                            score = max(
                                (
                                    v
                                    for k, v in prediction.items()
                                    if k.startswith(self.wake_word)
                                ),
                                default=0.0,
                            )

                            if score > max_score_seen:
                                max_score_seen = score

                            chunk_counter += 1
                            if chunk_counter % 62 == 0:
                                rms = float(
                                    np.sqrt(
                                        np.mean(audio_array.astype(np.float32) ** 2)
                                    )
                                )
                                logging.debug(
                                    f"Heartbeat | mic_rms={rms:.1f} | max_score_last_5s={max_score_seen:.4f}"
                                )
                                max_score_seen = 0.0

                            if score > 0.5:
                                logging.info(
                                    f"WAKE WORD TRIGGERED (score={score:.4f}) "
                                )
                                activeVoiceDetection.start()

                                oww_model.reset()
                                max_score_seen = 0.0
                                if self.running:
                                    self._update_status(
                                        f"Listening for '{self.wake_word.replace('_', ' ')}'..."
                                    )

                except Exception as loop_err:
                    if not self.running:
                        break  # Exit cleanly if stopped during an audio read
                    logging.warning(
                        f"Inner loop exception: {loop_err}\n{traceback.format_exc()}"
                    )
                    self._update_status(f"Audio error: {loop_err}")
                    time.sleep(1.0)

        except Exception as fatal_err:
            logging.error(f"FATAL thread crash: {fatal_err}\n{traceback.format_exc()}")
            self._update_status(f"Fatal voice error: {fatal_err}")
        finally:
            self.running = False

    @staticmethod
    def find_input_device(name_substring: str):
        """Finds the first input device index matching the given name substring."""
        if not name_substring:
            return None  # Falls back to system default

        for idx, dev in enumerate(sd.query_devices()):
            if (
                dev["max_input_channels"] > 0
                and name_substring.lower() in dev["name"].lower()
            ):
                logging.debug(f"Matched audio device [{idx}]: {dev['name']}")
                return idx

        logging.warning(
            f"Device '{name_substring}' not found. Falling back to system default."
        )
        return None


@st.cache_resource
def _get_worker():
    logging.debug("Creating cached _VoiceWorker singleton...")
    return _VoiceWorker(
        model_path="hey_cookbook.onnx", device=None, output_file="command.wav"
    )


def start(ui_container=None):
    """Call this from main.py to start or resume passive listening in the background."""
    worker = _get_worker()
    worker.start()


def stop():
    """Call this from main.py to stop passive listening and release the microphone."""
    worker = _get_worker()
    worker.stop()
