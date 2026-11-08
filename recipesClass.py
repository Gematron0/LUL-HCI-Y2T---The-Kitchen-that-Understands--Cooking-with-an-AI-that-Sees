import logging

class Recipes:
    """
    A class to represent a recipe with its details.
    """
    def __init__(self, recipe_id, name, imagePath, NumberOfServings) -> None:
        self.recipe_id = int(recipe_id)
        self.name = str(name)
        self.Steps = []
        self.TotalSteps = 0
        self.ImagePath = imagePath
        self.NumberOfServings = NumberOfServings
        self.Ingredient = []
        logging.debug(f"Created Recipe with ID: {self.recipe_id}, and name {self.name}")

    def get_recipe_id(self) -> int:
        return self.recipe_id

    def get_name(self) -> str:
        return self.name

    def Add_Step(self, StepNumber, StepTitle, StepInstructions, ImagePath, X, Y):
        NewStep = Steps(StepNumber, StepTitle, StepInstructions, ImagePath, X, Y)
        self.Steps.append(NewStep)
        self.TotalSteps += 1

    def Get_step(self, i):
        return self.Steps[i]

    def GetTotalSteps(self) -> int:
        return self.TotalSteps

    def GetImagePath(self) -> str:
        return self.ImagePath

    def getNumberOfServings(self) -> int:
        return self.NumberOfServings

    def Add_Ingredient(self, Ingredient, Quantity, Unit):
        NewIngredient = Ingredient(Ingredient, Quantity, Unit)
        self.Ingredient.append(NewIngredient)
        return

    def Get_Ingredients(self):
        return self.Ingredient



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

    def getStepTitle(self) -> str:
        return self.StepTitle 

    def getStepInstructions(self) -> str:
        return self.StepInstructions 

    def getImagePath(self) -> str:
        return self.ImagePath 

    def getImageCenter(self) -> list:
        return self.ImageCenter


class Ingredient():
    def __init__(self, Ingredient, Quantity, Unit) -> None:
        self.Ingredient = Ingredient
        self.Quantity = Quantity
        self.Unit = Unit

        logging.debug(f"Created a new Ingredient: {Ingredient} with {Quantity} {Unit}")

    def getIngredient(self) -> str:
        return self.Ingredient

    def getQuantity(self) -> str:
        return self.Quantity

    def getUnit(self) -> float:
        return self.Unit
