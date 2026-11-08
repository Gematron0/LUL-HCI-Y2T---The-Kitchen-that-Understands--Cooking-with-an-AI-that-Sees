# plugin imports
import logging
import os
import sys

parent_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.abspath(parent_dir))
import filesInitialise

import RecepyManigment.createARecipe as createARecipe
import RecepyManigment.deleteARecipe as deleteARecipe
import RecepyManigment.addAStepToRecipe as addAStepToRecipe
import RecepyManigment.deleteAStepFromRecipe as deleteAStepFromRecipe


def Main():
    logging.debug(f"Program started! [PID: {os.getpid()}]")

    # check the files to see if they exist and if not, create them
    logging.debug(f"Checking if the root file exists, if not create it.")

    filesInitialise.CheckIfRootFileExists()

    # asking the person what they would want to do
    logging.debug(f"Asking the person what they would want to do.")
    Action = input("What would you like to do? ('CREATE' - Create new recipe, 'DELETE' - delete existing recipes, '(AS) ADDSTEP' - add steps to existing recipe), '(DS) DELETESTEP' - delete steps from existing recipe): ")
    logging.debug(f"Action selected: {Action}")

    if Action == "CREATE" or Action == "C":
        logging.debug(f"Creating new recipe.")

        # asking user for basic input information
        logging.debug(f"Asking user for basic input information.")
        RecipeName = input("Enter the name of the recipe (STR): ")
        logging.debug(f"Recipe name entered: {RecipeName}")
        NumberOfSteps = int(input("Enter the number of steps in the recipe (INT) (you can add more once created): "))
        logging.debug(f"Number of steps entered: {NumberOfSteps}")

        # creating the recipe
        createARecipe.CreateRecipe(RecipeName, NumberOfSteps)

    elif Action == "DELETE" or Action == "D":
        logging.debug(f"Deleting existing recipe.")

        # asking user for the recipe ID to delete
        RecipeID = int(input("Enter the ID of the recipe to delete (INT): "))
        logging.debug(f"Recipe ID entered: {RecipeID}")
        deleteARecipe.DeleteRecipe(RecipeID)

    elif Action == "ADDSTEP" or Action == "AS":
        logging.debug(f"Adding steps to existing recipe.")

        # asking user for the recipe ID to add steps to
        RecipeID = int(input("Enter the ID of the recipe to add steps to (INT): "))
        logging.debug(f"Recipe ID entered: {RecipeID}")
        AddedStepLocation = input("Enter the step number location (or '++' if appending) (INT or STR): ")
        logging.debug(f"Step location entered: {AddedStepLocation}")
        addAStepToRecipe.AddAStep(RecipeID, AddedStepLocation)

    elif Action == "DELETESTEP" or Action == "DS":
        logging.debug(f"Removing steps from existing recipe.")

        # asking user for the recipe ID to remove steps from
        RecipeID = int(input("Enter the ID of the recipe to remove steps from (INT): "))
        logging.debug(f"Recipe ID entered: {RecipeID}")
        RemovedStepLocation = int(input("Enter the step number location to remove (INT): "))
        logging.debug(f"Step location entered: {RemovedStepLocation}")
        deleteAStepFromRecipe.DeleteAStep(RecipeID, RemovedStepLocation)

    else:
        logging.error(f"Invalid action selected: {Action}. Expected 'CREATE', 'DELETE', 'ADDSTEP', or 'DELETESTEP'.")
        print("Invalid action. Please select 'CREATE', 'DELETE', 'ADDSTEP', or 'DELETESTEP'.")
        sys.exit(1)


if __name__ == "__main__":
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s] [%(asctime)s] [%(filename)s | %(funcName)s()] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # call the main function
    Main()