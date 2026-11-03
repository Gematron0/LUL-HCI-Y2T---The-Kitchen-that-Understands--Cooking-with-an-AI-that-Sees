import os
from pathlib import Path
import logging
import json
import sys

import RecipeJSONFileDefaults as JSONRecipeDefaults

def AddAStep(RecipeID, StepLocation):
    """
    Add a step to an existing recipe.

    Parameters:
    RecipeID (int): The ID of the recipe to add a step to.
    StepLocation (int or str): The location to add the step. If '++', append to the end.

    Returns:
    None
    """

    # checking if the input data is valid
    if not isinstance(RecipeID, int):
        logging.error(f"Invalid input for RecipeID: {RecipeID}. Expected an integer.")
        raise ValueError("RecipeID must be an integer.")

    if not isinstance(StepLocation, (int, str)):
        logging.error(f"Invalid input for StepLocation: {StepLocation}. Expected an integer or '++'.")
        raise ValueError("StepLocation must be an integer or '++'.")

    # entering the recipe folder
    logging.debug(f"Attempting to add a step to recipe folder with ID: {RecipeID}")

    try:
        TargetFolder = Path.cwd() / "Recipes" / str(RecipeID)
        os.chdir(TargetFolder)
    except FileNotFoundError:
        logging.error(f"Recipe folder not found for ID: {RecipeID}")
        raise
    logging.debug(f"Changed working directory to: {os.getcwd()}")

    # checking the existing step files for all the step numbers
    ExistingSteps = [file.stem for file in Path.cwd().glob("*.json") if file.is_file()]

    ExistingSteps.remove("RecipeInfo")
    logging.debug(f"Existing steps found: {ExistingSteps}")

    ExistingStepsFixed = []
    for i, step in enumerate(ExistingSteps):
        ExistingStepsFixed.append(int(step.split("Step_")[1]))
        logging.debug(f"Processing step: {step} to {ExistingStepsFixed[i]}")

    ExistingSteps = ExistingStepsFixed
    logging.debug(f"Existing steps after processing: {ExistingSteps}")

    # if we just need to append the step to the end of the recipe
    if StepLocation == "++":
        StepLocation = max(ExistingSteps) + 1 if ExistingSteps else 1
        logging.debug(f"Appending new step at location: {StepLocation}")

        StepInfo = JSONRecipeDefaults.getStepInfoDefault(StepLocation)
        StepFilePath = Path.cwd() / f"Step_{StepLocation}.json"

        with open(StepFilePath, 'w') as StepFile:
            json.dump(StepInfo, StepFile, indent=4)
        logging.debug(f"Wrote step info to file: {StepFilePath}")

    # adding a step to the middle of the recipe, we need to move all the steps after the location up by 1
    else:
        logging.debug(f"Step location {StepLocation} exists. Shifting steps up by 1.")

        for step in sorted(ExistingSteps, reverse=True):
            if step >= int(StepLocation):
                OldFilePath = Path.cwd() / f"Step_{step}.json"
                NewFilePath = Path.cwd() / f"Step_{step + 1}.json"
                os.rename(OldFilePath, NewFilePath)
                logging.debug(f"Renamed {OldFilePath} to {NewFilePath}")

        StepInfo = JSONRecipeDefaults.getStepInfoDefault(StepLocation)
        StepFilePath = Path.cwd() / f"Step_{StepLocation}.json"

        with open(StepFilePath, 'w') as StepFile:
            json.dump(StepInfo, StepFile, indent=4)
        logging.debug(f"Wrote step info to file: {StepFilePath}")