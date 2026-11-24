# this file contains AI (for specifically downloading the model)

from transformers import pipeline
import logging
import time
import re

import Tools.getAllItems as getAllItems
import convertRecipesIntoClass


# downloading the model 
DEFAULT_INTENTS = ["allergens", "cooking equipment", "idk", "customer support"]
_classifier = None

def _get_classifier():
    """Lazy-loads the model once so it doesn't reload on every run()."""
    global _classifier
    if _classifier is None:
        _classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    return _classifier

def downlodeQuickUnderstand():
    _get_classifier()

def set_intents(intents: list[str]):
    """Updates the default intents list in quickSearch."""
    global SCANNED_INTENTS
    SCANNED_INTENTS = list(intents)


# running the model
def run(sentence: str) -> str | None:
    logging.info("started calculating what the person wants")
    startTime = time.time()

    global SCANNED_INTENTS
    try:
        SCANNED_INTENTS # type: ignore
    except NameError:
        logging.error("Scanned interests is not defined, therefore there can be no query, VOIDED")
        return ""
    if len(SCANNED_INTENTS) == 1:
        return str(SCANNED_INTENTS[0])

    classifier = _get_classifier()
    result = classifier(sentence, SCANNED_INTENTS)
    top_intent = result["labels"][0] # type: ignore
    confidence = result["scores"][0] # type: ignore

    logging.info(f"Intent: {top_intent} ({confidence:.2%})")
    logging.debug(f"time: {time.time()-startTime}")
    return str(top_intent)

# info extraction
def infoExtraction(type, sentence: str):

    CleanSentence = f" {re.sub(r'[^\w\s]', '', sentence.lower())} "

    match type:
        case None:
            return None

        case "List of allergens":
            FoundItems = set()
            for item in (x.lower() for x in getAllItems.getAllAllergen(convertRecipesIntoClass.get_recipes())):
                logging.debug(f"comparing {item} with {CleanSentence}")
                if f" {item} " in CleanSentence:
                    FoundItems.add(item)

                return FoundItems

        case "Go back a step":
            return ""

