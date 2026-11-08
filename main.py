# plugin imports
import logging
import os
import time
import streamlit as st

# file imports
import filesInitialise
import convertRecipesIntoClass
import searchRecipes

def main():
    logging.debug(f"Program started! [PID: {os.getpid()}]")

    # check the files to see if they exist and if not, create them
    filesInitialise.CheckIfRootFileExists()

    # creating the ui
    AppUi = st.container()

    # lode up all the recipes so that it can get displayed inside of the streamlit app into a class
    AllRecipes, RecipeKeys = convertRecipesIntoClass.ConvertRecipesIntoClass(AppUi)

    
    # how to get elements form the class
    # logging.warning(f"{AllRecipes[RecipeKeys["test3"]].GetTotalSteps()}")
    # logging.warning(f"{AllRecipes[RecipeKeys["test3"]].Get_step(1).getStepTitle()}")

    searchQuery = {"Text": ["TeSt1", "3"], "Equipment": ["another test", "hello there"]}
    print(searchQuery)
    searchRecipes.searchRecipes(searchQuery, AllRecipes, RecipeKeys)

if __name__ == "__main__":
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s] [%(asctime)s] [%(filename)s | %(funcName)s()] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # call the main function
    main()