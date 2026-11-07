from pathlib import Path
import os
import logging

def CheckIfRootFileExists():
    """
    Check if the root file exists, if not create it.
    """

    current_file_dir = Path(__file__).resolve().parent
    recipes_folder_path = current_file_dir / "Recipes"

    logging.debug("Checking if the recipes folder exists")
    if not os.path.exists("Recipes"):
        logging.warning("Recipes folder does not exist, creating it... (if this is the first time launching the program, this is normal)")
        recipes_folder_path.mkdir(parents=True, exist_ok=True)
        return

    logging.debug("Recipes folder exists, continuing")
    return