import os
from pathlib import Path
import logging
import json
import sys

import RecipeJSONFileDefaults as JSONRecipeDefaults

def CreateRecipe(Name, NSteps):
    """
    Create a new recipe with the given name and number of steps.

    Parameters:
    Name (str): The name of the recipe.
    NSteps (int): The number of steps in the recipe.

    Returns:
    folder: A folder and file containing basic information about the recipe
    """

    # checking in the input data is valid
    if not isinstance(Name, str):
        logging.error(f"Invalid input for Name: {Name}. Expected a string.")
        raise ValueError("Name must be a string.")

    if not isinstance(NSteps, int):
        logging.error(f"Invalid input for NSteps: {NSteps}. Expected an integer.")
        raise ValueError("NSteps must be an integer.")

    # entering the recipe folder
    logging.debug(f"Creating a new recipe folder with the name: {Name}")

    TargetFolder = Path.cwd() / "Recipes"
    os.chdir(TargetFolder)
    logging.debug(f"Changed working directory to: {os.getcwd()}")

    # checking the next folder number
    FolderName = [f.name for f in os.scandir() if f.is_dir()]
    logging.debug(f"Existing recipe folders: {FolderName}")

    # checking if there are 0 folders since thats a new program then
    if len(FolderName) == 0:
        logging.warning(f"No existing recipe folders found. Creating the first recipe folder. (this is normal if this is the first time launching the program)")
        NewFolderName = "0"

    # there are existing folders so we need to find the next number
    else:
        logging.debug(f"Existing recipe folders found. Finding the next available folder number.")
        FolderNumbers = [int(f) for f in FolderName if f.isdigit()]
        NewFolderNumber = max(FolderNumbers) + 1
        NewFolderName = str(NewFolderNumber)
        
    logging.debug(f"Next available folder number: {NewFolderName}")

    Path(NewFolderName).mkdir(parents=True, exist_ok=True)
    logging.debug(f"Created new recipe folder: {NewFolderName}")

    # entering the new recipe folder
    os.chdir(NewFolderName)
    logging.debug(f"Changed working directory to new recipe folder: {os.getcwd()}")

    # writing information as a dictionary to the .json file
    RecipeInfo = JSONRecipeDefaults.getRecipeInfoDefault(Name)
    logging.debug(f"Recipe info to be written to file: {RecipeInfo}")

    # creating a .json file that containing the recipe name image path and other basic information about the recipe
    RecipeFilePath = Path.cwd() / "RecipeInfo.json"
    logging.debug(f"Creating a new recipe info file at: {RecipeFilePath}")

    with open(RecipeFilePath, 'w') as RecipeFile:
        json.dump(RecipeInfo, RecipeFile, indent=4)
    logging.debug(f"Wrote recipe info to file: {RecipeFilePath}")


    # creating the step folders and writing the step information to a .json file
    for i in range(NSteps):

        StepInfo = JSONRecipeDefaults.getStepInfoDefault(i)

        StepFolderName = f"Step_{i}"
        StepFilePath = Path.cwd() / f"Step_{i}.json"

        with open(StepFilePath, 'w') as StepFile:
            json.dump(StepInfo, StepFile, indent=4)
        logging.debug(f"Wrote step info to file: {StepFilePath}")

    logging.info(f"Successfully created recipe '{Name}' with {NSteps} steps with ID: {NewFolderName}")
    sys.exit(0)