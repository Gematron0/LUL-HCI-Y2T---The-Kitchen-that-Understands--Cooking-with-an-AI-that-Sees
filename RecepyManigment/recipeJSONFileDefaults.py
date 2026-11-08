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
        "DisplayRecipeInSearch": "False",
        "ImagePath": "",
        "ImageCenter": [0, 0],
    }

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