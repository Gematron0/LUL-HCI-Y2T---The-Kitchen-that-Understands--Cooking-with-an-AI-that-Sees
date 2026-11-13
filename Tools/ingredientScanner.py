# this file contains AI

from ultralytics import YOLO
from ultralytics.engine.results import Results as YOLOResults
import logging
import time

def ImageToIngredientScanner(ImagePath, TargetIngredients) -> set:
    logging.info(f"Started Image to ingredient scanning")
    StartTime = time.time()

    try: 
        TargetIngredients = list(TargetIngredients)
    except:
        pass

    if not isinstance(TargetIngredients, list):
        logging.error(f"TargetIngredients must be a list; got: {type(TargetIngredients)}")
        raise ValueError("TargetIngredients must be an list.")

    if not isinstance(ImagePath, str):
        logging.error(f"ImagePath must be a str; got: {type(ImagePath)}")
        raise ValueError("ImagePath must be an str.")

    model = YOLO("yolov8x-worldv2.pt")

    set_classes = model.set_classes
    if set_classes is None:
        raise RuntimeError("The loaded model does not support setting classes.")
    
    set_classes(TargetIngredients)

    Predictions = model.predict(ImagePath, conf=0.2, iou=0.5, agnostic_nms=False)

    logging.debug(f"AI results: {Predictions}")

    FoundIngredient = set()
    for result in Predictions:
        if not isinstance(result, YOLOResults):
            raise TypeError(f"Expected YOLO results, got {type(result).__name__}.")

        if result.boxes is not None:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                name = model.names[cls_id]
                FoundIngredient.add(name)
            
    logging.info(f"Completed, time: {time.time()-StartTime}")
    logging.info(f"cleaned up results: {FoundIngredient}")
    return FoundIngredient