from pathlib import Path
import os
import logging

def CheckIfRootFileExists():
    """
    Check if the root file exists, if not create it.
    """

    logging.debug("Checking if the recipes folder exists")
    if not os.path.exists("Recipes"):
        logging.warning("Recipes folder does not exist, creating it... (if this is the first time launching the program, this is normal)")
        os.makedirs("Recipes")
        return

    logging.debug("Recipes folder exists, continuing")
    return