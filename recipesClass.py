import logging

class Recipes:
    """
    A class to represent a recipe with its details.
    """
    def __init__(self, r_id, n, ip, nos) -> None:
        self.recipe_id = int(r_id)
        self.name = str(n)
        self.Steps = []
        self.TotalSteps = 0
        self.ImagePath = ip
        self.NumberOfServings = nos
        self.Ingredients = []
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

    def Add_Ingredient(self, i, q, u):
        NewIngredient = Ingredient(i, q, u)
        self.Ingredients.append(NewIngredient)
        return

    def Get_Ingredients(self) -> list:
        return self.Ingredients



class Steps:
    def __init__(self, sn, st, si, ip, X, Y):
        self.StepNumber = int(sn)
        self.StepTitle = str(st)
        self.StepInstructions = str(si)
        self.ImagePath = str(ip)

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
    def __init__(self, i, q, u) -> None:
        self.Ingredient = str(i)
        self.Quantity = float(q)
        self.Unit = str(u)

        logging.debug(f"Created a new Ingredient: {self.Ingredient} with {self.Quantity} {self.Unit}")

    def getIngredient(self) -> str:
        return self.Ingredient

    def getQuantity(self) -> float:
        return self.Quantity

    def getUnit(self) -> str:
        return self.Unit
