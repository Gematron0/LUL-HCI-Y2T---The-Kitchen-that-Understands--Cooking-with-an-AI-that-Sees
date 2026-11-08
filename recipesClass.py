import logging

class Recipes:
    """
    A class to represent a recipe with its details.
    """
    def __init__(self, recipe_id, name) -> None:
        self.recipe_id = int(recipe_id)
        self.name = str(name)
        self.Steps = []
        self.TotalSteps = 0
        logging.debug(f"Created Recipe with ID: {self.recipe_id}, and name {self.name}")

    def get_recipe_id(self) -> int:
        return self.recipe_id

    def get_name(self) -> str:
        return self.name

    def Add_Step(self, StepNumber, StepTitle, StepInstructions, ImagePath, X, Y):
        NewStep = Steps(StepNumber, StepTitle, StepInstructions, ImagePath, X, Y)
        self.Steps.append(NewStep)
        logging.debug(f"New Step Created: {NewStep} now saved in: {self.Steps}")
        self.TotalSteps += 1

    def Get_step(self, i):
        return self.Steps[i]

    def GetTotalSteps(self) -> int:
        return self.TotalSteps



class Steps:
    def __init__(self, StepNumber, StepTitle, StepInstructions, ImagePath, X, Y):
        self.StepNumber = int(StepNumber)
        self.StepTitle = str(StepTitle)
        self.StepInstructions = str(StepInstructions)
        self.ImagePath = str(ImagePath)

        self.ImageCenter = []
        self.ImageCenter.append(X)
        self.ImageCenter.append(Y)
        logging.debug(f"Created a new Step: {self.StepNumber}, \nWith title: {self.StepTitle} \nAnd instructions: {StepInstructions}")
