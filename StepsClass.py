import logging

class Steps:
    def __init__(self, StepNumber, StepTitle, StepInstructions, ImagePath, X, Y):
        self.StepNumber = int(StepNumber)
        self.StepTitle = str(StepTitle)
        self.StepInstructions = str(StepInstructions)
        self.ImagePath = str(ImagePath)

        self.ImageCenter = []
        self.ImageCenter.append(X)
        self.ImageCenter.append(Y)
        logging.info(f"Created a new Step: {self.StepNumber}, \nWith title: {self.StepTitle} \nAnd instructions: {StepInstructions}")