from ultralytics import YOLO
from ultralytics.engine.results import Results as YOLOResults
import logging
import time

def downlodeSubPrograms() -> None:
    Start = time.time()
    logging.info(f"Downloading yolov8x-worldv2.pt")
    YOLO("yolov8x-worldv2.pt")
    logging.info(f"DownLode compleat; time: {Start-time.time()}")
    return