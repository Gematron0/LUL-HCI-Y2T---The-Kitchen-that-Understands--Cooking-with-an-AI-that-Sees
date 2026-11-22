import Tools.ingredientScanner as ingredientScanner
import Tools.speechToText as speechToText
import Tools.textToSpeech as textToSpeech

def downlodeSubPrograms() -> None:

    # downlode ingredient scanner model
    ingredientScanner.downlodeIngredientScannerModel()

    # speech to text model
    speechToText.downlodeSpeechToTextModel()

    # text to speech voice
    textToSpeech.downlodeTextToSpeechModel()
    return
