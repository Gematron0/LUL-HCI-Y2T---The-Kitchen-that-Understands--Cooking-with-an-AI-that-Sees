import logging

def getAllIngredient(RecipesClass) -> set:

    logging.info("Returning all ingredients")

    result = set()

    for Recipe in RecipesClass:
        logging.debug(f"on: {Recipe.get_name()}")
        IngredientObj = Recipe.Get_Ingredients()

        for Ingredients in IngredientObj:
            result.add(Ingredients.getIngredient())

    logging.info(f"compleat: {result}")

    return result

def getAllEquipment(RecipesClass) -> set:

    logging.info("Returning all equipment")

    result = set()

    for Recipe in RecipesClass:
        logging.debug(f"on: {Recipe.get_name()}")
        EquipmentObj = Recipe.get_Equipment()
        result.update(EquipmentObj)

    logging.info(f"compleat: {result}")
    return result

def getAllAllergen(RecipesClass) -> set:

    logging.info("Returning all allergen")

    result = set()

    for Recipe in RecipesClass:
        logging.debug(f"on: {Recipe.get_name()}")
        AllergensObj = Recipe.get_Allergies()
        result.update(AllergensObj)

    logging.info(f"compleat: {result}")
    return result
