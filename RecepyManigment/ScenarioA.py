import json
from pathlib import Path
import os
import logging

def ScenarioA():

    """
    Allows the user to enter multiple ingredients and searches saved
    recipes for those containing all the entered ingredients.
    Displays matching recipes or informs the user if none are found.

    Solves Scenario A: "What can I cook with this?"
    """
    Targetfolder = Path.cwd() #recipes folder to check if the ingredient is in any recipe or not
    os.chdir(Targetfolder)
    matching_recipe_files=set()
    files=[]
    Ingredient_name= []
    for recipe_folder in Targetfolder.iterdir():
        info_file = recipe_folder / "RecipeInfo.json"
        if info_file.is_file():
            files.append(info_file)
            
    while True:
            ingredient = input("Enter an ingredient (or type 'done' to finish): ").strip().casefold()
            if ingredient == "done":
                break
            if ingredient != "":
                Ingredient_name.append(ingredient)

    if not Ingredient_name:
            print("Please enter at least one ingredient.")
            return

    for i in files:
        with open(i,'r') as recipe_file:
            data=json.load(recipe_file)
            Ingredients=data["Ingredients"]
            if all(
                name.casefold() in [j[0].casefold() for j in Ingredients]
                for name in Ingredient_name
                ):
                matching_recipe_files.add(data["RecipeName"])

    if not matching_recipe_files:
        print("No matching recipe")
    else:
        print(matching_recipe_files)
