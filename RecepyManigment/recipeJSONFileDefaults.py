def getRecipeInfoDefault(Name):
    """
    Get the default recipe information for a given recipe name.

    Parameters:
    name (str): The name of the recipe.

    Returns:
    dict: A dictionary containing the default recipe information.
    """
    return {
        "RecipeName": Name,
        "DisplayRecipeInSearch": False,
        "ImagePath": "",
        "ImageCenter": [0, 0],
        "Servings": 4
    }

def getEquipmentInfoDefault():
    return ["", "", ""]

def getIngredientsInfoDefault():
    """
    Get the default recipe information for a given recipe name.

    Parameters:
    name (str): The name of the recipe.

    Returns:
    dict: A dictionary containing the default recipe information.
    """
    return [{"ingredient": "", "amount": "", "type": ""}, {"ingredient": "", "amount": "", "type": ""}]

def getAllergenInfoDefault():
    return ["", "", ""]


def getStepInfoDefault(StepNumber):
    """
    Get the default step information for a given step number.

    Parameters:
    step_number (int): The step number.

    Returns:
    dict: A dictionary containing the default step information.
    """
    return {
        "Title": f"Step {StepNumber}",
        "Text": "Sample text for the step",
        "ImagePath": "",
        "ImageCenter": [0, 0],
    }