# plugin imports
import logging
import os
import time
import streamlit as st
import sys
import speech_recognition as sr

# file imports
import filesInitialise
import convertRecipesIntoClass
import Tools.searchRecipes as searchRecipes
import Tools.ingredientScanner as ingredientScanner
import Tools.downlodeSubPrograms as downlodeSubPrograms
import Tools.getAllItems as getAllItems
import Tools.speechToText as speechToText
import Tools.VoiceModule.passiveVoiceDetection as passiveVoiceDetection
import Tools.VoiceModule.activeVoiceDetection as activeVoiceDetection


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

    # code function that you need below hear
    # activeVoiceDetection.start()


if __name__ == "__main__":
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s] [%(asctime)s] [%(filename)s | %(funcName)s()] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # call the main function
    main()


