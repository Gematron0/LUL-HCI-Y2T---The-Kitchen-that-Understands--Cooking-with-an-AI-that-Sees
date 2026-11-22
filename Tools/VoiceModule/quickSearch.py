from transformers import pipeline
import logging
import time

def downlodeQuickUnderstand():
    pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def run(sentence: str) -> str | None:
    logging.info("started calculating what the person wants")
    startTime = time.time()
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    possible_intents = ["allergens", "cooking equipment", "idk", "customer support"]

    result = classifier(sentence, possible_intents)

    # Print the top predicted intent and its confidence score
    top_intent = result["labels"][0]
    confidence = result["scores"][0]

    logging.info(f"Intent: {top_intent} ({confidence:.2%})")

    print(f"Intent: {top_intent} ({confidence:.2%})")
    print(f"time: {time.time()-startTime}")
    if confidence >= 40:
        return None
    
    return top_intent