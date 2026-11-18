import logging
import os
import threading
import time
import traceback
import numpy as np
import sounddevice as sd
import speech_recognition as sr
import streamlit as st
from openwakeword.model import Model


class _VoiceWorker:
    def __init__(self, model_path="hey_cookbook.onnx", device=4):
        self.model_path = model_path
        self.wake_word = os.path.splitext(os.path.basename(model_path))[0]
        self.device = device
        self.status = f"Initializing '{self.wake_word.replace('_', ' ')}'..."
        self.last_command = ""
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
            recognizer = sr.Recognizer()

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
                                # Immediately record 5 seconds using the already-open stream
                                self._record_and_transcribe(stream, recognizer, RATE, CHUNK)
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

    def _record_and_transcribe(self, stream, recognizer, rate, chunk_size):
        DURATION = 5  # Seconds to record
        total_chunks = int((rate * DURATION) / chunk_size)  # 62 chunks (~5.0s)
        frames = []

        logging.info(f"[_record_and_transcribe] Recording {DURATION}s ({total_chunks} chunks) immediately...")

        try:
            for i in range(total_chunks):
                if not self.running:
                    return
                # Update countdown in the UI every ~1 second
                if i % 12 == 0:
                    seconds_left = max(1, DURATION - int((i * chunk_size) / rate))
                    with self.lock:
                        self.status = f"🎙️ Speak now! Recording ({seconds_left}s)..."

                data, _ = stream.read(chunk_size)
                frames.append(bytes(data))

            raw_audio = b"".join(frames)
            logging.info(f"[_record_and_transcribe] Finished 5s recording ({len(raw_audio)} bytes).")

            with self.lock:
                self.status = "Processing speech..."

            audio_data = sr.AudioData(raw_audio, rate, 2)
            command_text = recognizer.recognize_google(audio_data)
            logging.info(f"[_record_and_transcribe] Transcription: '{command_text}'")

            with self.lock:
                self.last_command = command_text

        except sr.UnknownValueError:
            logging.info("[_record_and_transcribe] Speech was unintelligible.")
            with self.lock:
                self.status = "Could not understand command."
            time.sleep(1.5)
        except sr.RequestError as req_err:
            logging.info(f"[_record_and_transcribe] Speech API error: {req_err}")
            with self.lock:
                self.status = "Speech recognition service error."
            time.sleep(1.5)
        except Exception as e:
            logging.info(f"[_record_and_transcribe] Unexpected error: {e}\n{traceback.format_exc()}")
            with self.lock:
                self.status = "Error processing speech."
            time.sleep(1.5)


@st.cache_resource
def _get_worker():
    logging.info("[_get_worker] Creating cached _VoiceWorker singleton...")
    worker = _VoiceWorker(model_path="hey_cookbook.onnx", device=4)
    worker.start()
    return worker


def start(ui_container=None):
    """Call this from main.py to start passive listening and render status."""
    worker = _get_worker()
    target = ui_container if ui_container is not None else st

    @st.fragment(run_every="0.5s")
    def _voice_status_ui():
        with worker.lock:
            status = worker.status
            command = worker.last_command

        with target:
            st.caption(f"🎙️ **Voice Assistant:** {status}")
            if command:
                st.info(f"**Last Voice Command:** {command}")

    _voice_status_ui()


def get_latest_command():
    worker = _get_worker()
    with worker.lock:
        cmd = worker.last_command
        worker.last_command = ""
    return cmd