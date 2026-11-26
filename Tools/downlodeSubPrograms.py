import streamlit as st
import Tools.ingredientScanner as ingredientScanner
import Tools.speechToText as speechToText
import Tools.VoiceModule.quickSearch as quickSearch
import Tools.textToSpeech as textToSpeech

def downlodeSubPrograms(_subProgressBar) -> None:
    _subProgressBar.progress(0)

    # download ingredient scanner model
    ingredientScanner.downlodeIngredientScannerModel()
    _subProgressBar.progress(25)

    # speech to text model
    speechToText.downlodeSpeechToTextModel()
    _subProgressBar.progress(50)

    # quick search
    quickSearch.downlodeQuickUnderstand()
    _subProgressBar.progress(75)

    # text to speech voice
    textToSpeech.downlodeTextToSpeechModel()
    _subProgressBar.progress(100)