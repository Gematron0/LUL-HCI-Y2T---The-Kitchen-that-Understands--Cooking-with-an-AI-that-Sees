import os
from pathlib import Path
import logging
import shutil
import sys

def DeleteAStep(RecipeID, StepLocation):
    """
    Delete a step from an existing recipe.

    Parameters:
    RecipeID (int): The ID of the recipe to delete a step from.
    StepLocation (int): The location of the step to delete.

    Returns:
    None
    """

    # checking if the input data is valid
    if not isinstance(RecipeID, int):
        logging.error(f"Invalid input for RecipeID: {RecipeID}. Expected an integer.")
        raise ValueError("RecipeID must be an integer.")

    if not isinstance(StepLocation, int):
        logging.error(f"Invalid input for StepLocation: {StepLocation}. Expected an integer.")
        raise ValueError("StepLocation must be an integer.")

    # entering the recipe folder
    logging.debug(f"Attempting to delete a step from recipe folder with ID: {RecipeID}")

    try:
        current_file_dir = Path(__file__).resolve().parent
        recipes_folder_path = current_file_dir / ".." / "Recipes" / str(RecipeID)
        os.chdir(recipes_folder_path)
    except FileNotFoundError:
        logging.error(f"Recipe folder not found for ID: {RecipeID}")
        raise
    logging.debug(f"Changed working directory to: {os.getcwd()}")

    # checking if the step file exists
    StepFilePath = Path.cwd() / f"Step_{StepLocation}.json"
    if not StepFilePath.is_file():
        logging.error(f"Step file not found for StepLocation: {StepLocation} in RecipeID: {RecipeID}")
        raise FileNotFoundError(f"Step file not found for StepLocation: {StepLocation} in RecipeID: {RecipeID}")

    # deleting the step file
    StepFilePath.unlink()
    logging.info(f"Successfully deleted step {StepLocation} from recipe {RecipeID}")

    # renaming the subsequent step files to fill the gap
    ExistingSteps = [file.stem for file in Path.cwd().glob("*.json") if file.is_file() and file.stem != "RecipeInfo" and file.stem != "Ingredients"]
    ExistingStepsFixed = []
    for step in ExistingSteps:
        ExistingStepsFixed.append(int(step.split("Step_")[1]))

    ExistingSteps = ExistingStepsFixed
    for step in sorted(ExistingSteps):
        if step > StepLocation:
            OldFilePath = Path.cwd() / f"Step_{step}.json"
            NewFilePath = Path.cwd() / f"Step_{step - 1}.json"
            os.rename(OldFilePath, NewFilePath)
            logging.debug(f"Renamed {OldFilePath} to {NewFilePath}")

    logging.info(f"Successfully deleted step {StepLocation} and updated subsequent steps in recipe {RecipeID}")

    sys.exit(0)