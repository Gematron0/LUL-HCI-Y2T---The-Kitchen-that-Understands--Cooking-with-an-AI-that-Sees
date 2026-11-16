import Tools.ingredientScanner as ingredientScanner
import Tools.speechToText as speechToText

def downlodeSubPrograms() -> None:

    # downlode ingredient scanner model
    ingredientScanner.downlodeIngredientScannerModel()

    # speech to text model
    speechToText.downlodeSpeechToTextModel()
    return
