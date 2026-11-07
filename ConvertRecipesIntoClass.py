import streamlit as st
import time
import os
from pathlib import Path
import logging
import json

import RecipesClass

def ConvertRecipesIntoClass(AppUi):
    """
    This function converts all recipes into a class format for easier management and manipulation.
    It reads the existing recipe files, processes them, and saves them in a structured class format.
    It also worked on the UI for the streamlit app to show a progress bar while loading the recipes.
    """
    logging.debug("Starting the conversion of recipes into class format.")

    # creating the app UI
    ClassConversionUI = AppUi.container()

    AppProgressBar = ClassConversionUI.progress(0, text="Loading Recipes...")
    logging.debug("UI created for loading recipes with a progress bar.")

    # saveing the recipes into a class format
    CurrentFileDir = Path(__file__).resolve().parent
    RecipesDir = CurrentFileDir / "Recipes"
    logging.debug(f"Loading recipes from directory: {RecipesDir}")

    RecipeIDs = [int(folder.name) for folder in RecipesDir.iterdir() if folder.is_dir()]
    RecipeIDs.sort()
    logging.debug(f"Found recipe IDs: {RecipeIDs}")
    NumberOfRecipes = len(RecipeIDs)
    logging.debug(f"Total number of recipes: {NumberOfRecipes}")

    # going thru all the recipes
    AllRecipes = []
    for index, RecipeID in enumerate(RecipeIDs):
        logging.debug(f"Checking recipe {RecipeID}")

        CurrentFileDir = Path(__file__).resolve().parent
        RecipesDir = CurrentFileDir / "Recipes" / str(RecipeID)
        RecipeFilePath = RecipesDir / "RecipeInfo.json"

        with open(RecipeFilePath, "r", encoding="utf-8") as file:
            data = json.load(file)

        RecipeName = data.get("RecipeName")

        Recipes = RecipesClass.Recipes(RecipeID, RecipeName)

        # adding all of the steps
        json_steps = [file.name for file in RecipesDir.rglob("*.json") if file.name not in ["RecipeInfo.json","Ingredients.json"]]
        json_steps.sort()
        logging.debug(f"All steps found: {json_steps}")

        for i, step in enumerate(json_steps):
            RecipeFilePath = RecipesDir / step

            with open(RecipeFilePath, "r", encoding="utf-8") as file:
                data = json.load(file)

            StepTitle = data.get("Title")
            StepInstruction = data.get("Text")
            StepImage = data.get("ImagePath")
            StepImageCoordinates = data.get("ImageCenter")

            Recipes.Add_Step(i, StepTitle, StepInstruction, StepImage, StepImageCoordinates[0], StepImageCoordinates[1])

        # adding it to the total of all recipes
        AllRecipes.append(Recipes)

        # update the apps progress bar
        percentage = round((index/NumberOfRecipes), 2)
        AppProgressBar.progress(percentage, text=f"Loading Recipes... ({index}/{NumberOfRecipes})")

    AppProgressBar.empty()
    ClassConversionUI.empty()
    logging.info(f"Finished converting recipes")

    return AllRecipes
