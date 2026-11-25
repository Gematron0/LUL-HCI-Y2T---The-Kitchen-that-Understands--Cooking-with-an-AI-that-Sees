import Tools.ingredientScanner as ingredientScanner
import Tools.speechToText as speechToText
import Tools.VoiceModule.quickSearch as quickSearch
import Tools.textToSpeech as textToSpeech
import streamlit as st

@st.cache_resource
def downlodeSubPrograms() -> None:

    # downlode ingredient scanner model
    ingredientScanner.downlodeIngredientScannerModel()

    # speech to text model
    speechToText.downlodeSpeechToTextModel()

    # quick search
    quickSearch.downlodeQuickUnderstand()

    # text to speech voice
    textToSpeech.downlodeTextToSpeechModel()
    return
