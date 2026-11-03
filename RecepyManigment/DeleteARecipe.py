# this file contained AI generated code below line 42

import os
from pathlib import Path
import logging
import shutil
import sys

def DeleteRecipe(RecipeID):
    """
    Delete an existing recipe with the given ID.

    Parameters:
    RecipeID (int): The ID of the recipe to delete.

    Returns:
    None
    """

    # checking if the input data is valid
    if not isinstance(RecipeID, int):
        logging.error(f"Invalid input for RecipeID: {RecipeID}. Expected an integer.")
        raise ValueError("RecipeID must be an integer.")

    # entering the recipe folder
    logging.debug(f"Attempting to delete recipe folder with ID: {RecipeID}")

    TargetFolder = Path.cwd() / "Recipes"
    os.chdir(TargetFolder)
    logging.debug(f"Changed working directory to: {os.getcwd()}")

    # checking if the folder exists
    FolderName = str(RecipeID)
    if not os.path.isdir(FolderName):
        logging.error(f"Recipe folder with ID {RecipeID} does not exist.")
        raise FileNotFoundError(f"Recipe folder with ID {RecipeID} does not exist.")

    # deleting the folder and its contents
    shutil.rmtree(FolderName)
    logging.info(f"Successfully deleted recipe folder with ID: {RecipeID}")

    # Get all folders that are digits and greater than RecipeID
    folders_to_rename = []
    for item in TargetFolder.iterdir():
        if item.is_dir() and item.name.isdigit():
            folder_num = int(item.name)
            if folder_num > RecipeID:
                folders_to_rename.append((folder_num, item))

    # Sort the folders to rename in ascending order based to avoid overwriting 
    folders_to_rename.sort(key=lambda x: x[0])

    # Rename them safely from the highest number down
    for folder_num, old_path in folders_to_rename:
        new_folder_name = str(folder_num - 1)
        new_path = old_path.with_name(new_folder_name)
        
        try:
            old_path.rename(new_path)
            logging.debug(f"Renamed folder {old_path.name} to {new_folder_name}")
        except Exception as e:
            logging.error(f"Failed to rename {old_path.name} to {new_folder_name}: {e}")

    sys.exit(0)
