# audioManager.py

import sounddevice as sd
import threading
import logging
import queue


class AudioManager:

    def __init__(self, samplerate=48000, blocksize=1280, channels=1):

        self.samplerate = samplerate
        self.blocksize = blocksize
        self.channels = channels

        self.listeners = []

        self.running = False
        self.stream = None

        self.lock = threading.Lock()

    def subscribe(self, callback):

        with self.lock:
            self.listeners.append(callback)

    def unsubscribe(self, callback):

        with self.lock:
            if callback in self.listeners:
                self.listeners.remove(callback)

    def _audio_callback(self, indata, frames, time_info, status):

        if status:
            logging.warning(f"Audio status: {status}")

        audio_data = bytes(indata)

        with self.lock:
            listeners = list(self.listeners)

        for listener in listeners:
            try:
                listener(audio_data, frames)
            except Exception:
                logging.exception("Audio listener failed")

    def start(self, device=None):

        if self.running:
            return

        self.stream = sd.RawInputStream(
            samplerate=self.samplerate,
            blocksize=self.blocksize,
            channels=self.channels,
            dtype="int16",
            device=device,
            callback=self._audio_callback,
        )

        self.stream.start()
        self.running = True

        logging.info("Shared microphone started.")

    def stop(self):

        if not self.running:
            return

        self.stream.stop()
        self.stream.close()

        self.stream = None
        self.running = False

        logging.info("Shared microphone stopped.")
