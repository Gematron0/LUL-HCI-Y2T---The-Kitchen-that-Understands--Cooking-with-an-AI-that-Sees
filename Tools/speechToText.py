# this file contains AI

from faster_whisper import WhisperModel
import io
import logging
import os
import time

# the whisper model that is used, it gets downloaded by the code (so it dose not need to be inside of the git)
SpeechToTextModelName = "base"

# the model is kept hear after the first lode, so that it dose not need to be loaded again for every call
_LoadedModel = None

def downlodeSpeechToTextModel() -> None:
    """
    Downloads the speech to text model (if it is not downloaded yet) and lodes it into memory
    """
    Start = time.time()
    logging.info(f"Downloading speech to text model: {SpeechToTextModelName}")
    _getModel()
    logging.info(f"DownLode compleat; time: {time.time()-Start}")
    return

def SpeechToText(AudioInput, Language=None) -> str:
    """
    Converts spoken audio into text, used by the quick and complex voice systems

    Parameters:
    AudioInput (str | bytes | file like object): the audio that should get converted, where
        str: the path to an audio file (wav, mp3, m4a, ogg, flac ...)
        bytes: the raw content of an audio file
        file like object: an opened audio file, e.g. the result of streamlit st.audio_input()
    Language (str | None): the language code that is spoken (e.g. "en", "de"), if None the model detects it by itself

    Returns:
    str: the text that was spoken, an empty str if no speech was found inside of the audio
    """
    logging.info(f"Started speech to text")
    StartTime = time.time()

    # 1
    # validating that the input is right types
    if Language is not None and not isinstance(Language, str):
        logging.error(f"Language must be a str or None; got: {type(Language)}")
        raise ValueError("Language must be an str or None.")

    Audio = _prepareAudioInput(AudioInput)

    # 2
    # send the audio thru the AI
    model = _getModel()

    try:
        Segments, Info = model.transcribe(Audio, language=Language, vad_filter=True)

        # the segments are a generator, the audio only gets converted while going thru them
        FoundText = []
        for Segment in Segments:
            logging.debug(f"[{Segment.start:.2f}s -> {Segment.end:.2f}s] {Segment.text}")
            FoundText.append(Segment.text.strip())

    except Exception as Error:
        logging.error(f"The audio could not be converted to text: {Error}")
        raise RuntimeError("The audio could not be converted to text.") from Error

    # 3
    # combine all segments into one text
    Result = " ".join(Text for Text in FoundText if Text)

    logging.debug(f"Detected language: {Info.language} ({Info.language_probability:.2%})")
    logging.info(f"Completed, time: {time.time()-StartTime}")
    logging.info(f"Text: {Result}")
    return Result

def _prepareAudioInput(AudioInput):
    """
    Checks the audio input and converts it into something the model can read (a path or a file like object)
    """
    if isinstance(AudioInput, str):
        if not os.path.isfile(AudioInput):
            logging.error(f"Audio file dose not exist: {AudioInput}")
            raise FileNotFoundError(f"Audio file dose not exist: {AudioInput}")
        return AudioInput

    if isinstance(AudioInput, (bytes, bytearray)):
        if len(AudioInput) == 0:
            logging.error(f"AudioInput contains no data")
            raise ValueError("AudioInput must not be empty.")
        return io.BytesIO(AudioInput)

    if hasattr(AudioInput, "read"):
        # make sure the file gets read form the beginning, even if it was already read before
        if hasattr(AudioInput, "seek"):
            AudioInput.seek(0)
        return AudioInput

    logging.error(f"AudioInput must be a str, bytes or a file like object; got: {type(AudioInput)}")
    raise ValueError("AudioInput must be an str, bytes or a file like object.")

def _getModel() -> WhisperModel:
    global _LoadedModel

    if _LoadedModel is None:
        logging.debug(f"Loading speech to text model: {SpeechToTextModelName}")
        _LoadedModel = WhisperModel(SpeechToTextModelName, device="auto", compute_type="default")

    return _LoadedModel
