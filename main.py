# plugin imports
import logging
import os
import time
import streamlit as st

# file imports
import filesInitialise
import convertRecipesIntoClass
import Tools.search as search
import Tools.ingredientScanner as ingredientScanner
import Tools.downlodeSubPrograms as downlodeSubPrograms

def main():
    logging.debug(f"Program started! [PID: {os.getpid()}]")

    # check the files to see if they exist and if not, create them
    filesInitialise.CheckIfRootFileExists()

    # download all dependence
    downlodeSubPrograms.downlodeSubPrograms()

    # creating the ui
    AppUi = st.container()

    # lode up all the recipes so that it can get displayed inside of the streamlit app into a class
    AllRecipes, RecipeKeys = convertRecipesIntoClass.ConvertRecipesIntoClass(AppUi)

    
    # how to get elements form the class
    # logging.warning(f"{AllRecipes[RecipeKeys["test3"]].GetTotalSteps()}")
    # logging.warning(f"{AllRecipes[RecipeKeys["test3"]].Get_step(1).getStepTitle()}")
    AllRecipes[0].Add_Ingredient("Banana", 20, "g")
    AllRecipes[0].Add_Ingredient("Cherry", 50, "kg")
    AllRecipes[2].Add_Ingredient("Cherry", 50, "kg")
    AllRecipes[2].Add_Ingredient("Cherry", 50, "kg")
    AllRecipes[2].Add_Ingredient("Cherry", 50, "kg")

    ingredients = [
    "garlic",
    "yellow onion",
    "shallot",
    "scallion",
    "ginger",
    "carrot",
    "celery",
    "bell pepper",
    "jalapeno",
    "tomato",
    "cherry tomato",
    "spinach",
    "kale",
    "broccoli",
    "cauliflower",
    "zucchini",
    "potato",
    "sweet potato",
    "button mushroom",
    "cucumber",
    "basil",
    "cilantro",
    "parsley",
    "rosemary",
    "thyme",
    "oregano",
    "bay leaf",
    "cumin",
    "paprika",
    "cinnamon",
    "chicken breast",
    "ground beef",
    "salmon fillet",
    "shrimp",
    "tofu",
    "egg",
    "unsalted butter",
    "heavy cream",
    "milk",
    "parmesan cheese",
    "olive oil",
    "sesame oil",
    "soy sauce",
    "apple cider vinegar",
    "honey",
    "all-purpose flour",
    "white rice",
    "spaghetti",
    "black beans",
    "chicken broth",
]

    output = ingredientScanner.ImageToIngredientScanner("2ndtest.jpg",ingredients)

if __name__ == "__main__":
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s] [%(asctime)s] [%(filename)s | %(funcName)s()] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # call the main function
    main()