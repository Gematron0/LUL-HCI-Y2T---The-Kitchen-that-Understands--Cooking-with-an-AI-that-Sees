# passiveVoiceDetection.py

import logging
import os
import queue
import threading
import time

import av
import numpy as np
import streamlit as st

from openwakeword.model import Model
from streamlit_webrtc import WebRtcMode, webrtc_streamer

import Tools.VoiceModule.activeVoiceDetection as activeVoiceDetection


class _VoiceWorker:

    def __init__(
        self,
        model_path="hey_cookbook.onnx",
        output_file="command.wav",
        threshold=0.5,
        cooldown=3.0,
    ):

        self.model_path = model_path
        self.wake_word = os.path.splitext(os.path.basename(model_path))[0]

        self.output_file = output_file
        self.threshold = threshold
        self.cooldown = cooldown

        self.last_trigger_time = 0.0

        self.running = False
        self.thread = None

        self.lock = threading.Lock()

        self.web_audio_queue = queue.Queue(maxsize=100)

    def start(self):

        with self.lock:

            if self.running:
                return

            self.running = True

            self.thread = threading.Thread(
                target=self._listen_loop,
                name="VoiceListenerThread",
                daemon=True,
            )

            self.thread.start()

    def stop(self):

        with self.lock:

            if not self.running:
                return

            self.running = False
            thread_to_join = self.thread

        if (
            thread_to_join
            and thread_to_join.is_alive()
            and threading.current_thread() != thread_to_join
        ):
            thread_to_join.join(timeout=2.0)


    def push_browser_audio(self, pcm):

        if pcm.dtype != np.int16:
            pcm = pcm.astype(np.int16)

        CHUNK = 1280

        if not hasattr(self, "_audio_buffer"):
            self._audio_buffer = np.array([], dtype=np.int16)

        if not hasattr(self, "_audio_buffer_lock"):
            self._audio_buffer_lock = threading.Lock()

        chunks = []

        with self._audio_buffer_lock:

            self._audio_buffer = np.concatenate(
                (self._audio_buffer, pcm)
            )

            while len(self._audio_buffer) >= CHUNK:

                chunk = self._audio_buffer[:CHUNK].copy()

                self._audio_buffer = self._audio_buffer[CHUNK:]

                chunks.append(chunk)

        for chunk in chunks:

            try:
                self.web_audio_queue.put_nowait(chunk)

            except queue.Full:

                try:
                    self.web_audio_queue.get_nowait()
                    self.web_audio_queue.put_nowait(chunk)

                except queue.Empty:
                    pass

            try:
                activeVoiceDetection.feed_audio(chunk)

            except Exception:
                logging.exception(
                    "Could not forward audio to active detection"
                )


    def _listen_loop(self):

        logging.info("Initializing OpenWakeWord...")

        try:

            oww_model = Model(wakeword_model_paths=[self.model_path])

            logging.info(f"MODEL LOADED: {self.model_path}")

            logging.info(f"MODEL KEYS: {list(oww_model.models.keys())}")

            last_log_time = time.monotonic()
            max_score = 0.0

            while self.running:

                try:

                    audio_array = self.web_audio_queue.get(timeout=0.5)

                except queue.Empty:
                    continue

                try:

                    rms = float(np.sqrt(np.mean(audio_array.astype(np.float32) ** 2)))

                    prediction = oww_model.predict(audio_array)

                    scores = {k: float(v) for k, v in prediction.items()}

                    matching_scores = [
                        value
                        for key, value in scores.items()
                        if self.wake_word.lower() in key.lower()
                    ]

                    score = max(matching_scores, default=0.0)

                    max_score = max(max_score, score)

                    now = time.monotonic()

                    if now - last_log_time >= 1.0:

                        logging.info(
                            f"WAKE DEBUG | "
                            f"RMS={rms:.1f} | "
                            f"MAX_SCORE={max_score:.5f} | "
                            f"ALL_PREDICTIONS={scores}"
                        )

                        max_score = 0.0
                        last_log_time = now

                    # Detect wake word.
                    if (
                        score >= self.threshold
                        and now - self.last_trigger_time >= self.cooldown
                    ):

                        self.last_trigger_time = now

                        logging.warning(f"WAKE WORD DETECTED! Score={score:.5f}")

                        try:

                            # This now activates recording.
                            # It must NOT open another microphone.
                            activeVoiceDetection.start()

                        except Exception:

                            logging.exception("Could not activate command recording")

                        oww_model.reset()

                except Exception:

                    logging.exception("OpenWakeWord prediction error")

        except Exception:

            logging.exception("Fatal OpenWakeWord error")

        finally:

            self.running = False

            logging.info("Wake-word listener stopped.")


@st.cache_resource
def _get_worker():

    logging.debug("Creating cached VoiceWorker singleton")

    return _VoiceWorker(
        model_path="hey_cookbook.onnx",
        threshold=0.5,
        cooldown=3.0,
    )


def _render_browser_mic(device_id=None):

    worker = _get_worker()

    resampler = av.AudioResampler(
        format="s16",
        layout="mono",
        rate=16000,
    )

    frame_counter = 0

    def audio_frame_callback(frame):

        nonlocal frame_counter

        try:

            converted_frames = resampler.resample(frame)

            for converted in converted_frames:

                pcm = converted.to_ndarray().reshape(-1)

                if pcm.dtype != np.int16:
                    pcm = pcm.astype(np.int16)

                # One microphone source.
                # Both passive and active detection receive these frames.
                worker.push_browser_audio(pcm)

            frame_counter += 1

            if frame_counter % 100 == 0:

                logging.info(
                    f"Microphone active | "
                    f"frames={frame_counter} | "
                    f"input_rate={frame.sample_rate}"
                )

        except Exception:

            logging.exception("Microphone audio conversion failed")

        return frame

    audio_constraints = {
        "echoCancellation": True,
        "noiseSuppression": True,
        "autoGainControl": True,
    }

    if device_id:

        audio_constraints["deviceId"] = {"exact": device_id}

    st.markdown(
        """
        <style>
            div[data-testid="stCustomComponentV1"] {
                position: fixed !important;
                left: -10000px !important;
                top: 0 !important;
                width: 1px !important;
                height: 1px !important;
                opacity: 0 !important;
                overflow: hidden !important;
                pointer-events: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    webrtc_streamer(
        key="passive-wake-word-mic",
        mode=WebRtcMode.SENDONLY,
        audio_frame_callback=audio_frame_callback,
        media_stream_constraints={
            "video": False,
            "audio": audio_constraints,
        },
        desired_playing_state=True,
    )


def start():

    worker = _get_worker()

    worker.start()

    _render_browser_mic()


def stop():

    worker = _get_worker()

    worker.stop()
