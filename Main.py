# plugin imports
import logging
import os
import streamlit as st

# file imports
import FilesInitialise

def main():
    logging.debug(f"Program started! [PID: {os.getpid()}]")

    # check the files to see if they exist and if not, create them
    FilesInitialise.CheckIfRootFileExists()

    # lode up all the recipes so that it can get displayed inside of the streamlit app

if __name__ == "__main__":
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s] [%(asctime)s] [%(filename)s | %(funcName)s()] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # call the main function
    main()