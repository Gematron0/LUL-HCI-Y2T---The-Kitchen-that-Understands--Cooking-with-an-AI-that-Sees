import Tools.ingredientScanner as ingredientScanner
import Tools.speechToText as speechToText
import Tools.VoiceModule.quickSearch as quickSearch

def downlodeSubPrograms() -> None:

    # downlode ingredient scanner model
    ingredientScanner.downlodeIngredientScannerModel()

    # speech to text model
    speechToText.downlodeSpeechToTextModel()

    # quick search
    quickSearch.downlodeQuickUnderstand()
    return
