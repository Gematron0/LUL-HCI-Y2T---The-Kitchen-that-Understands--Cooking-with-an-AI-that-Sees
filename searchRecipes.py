import logging
import time

def searchRecipes(SearchQuery, RecipesClass, RecipeKeys) -> list:
    StartTime = time.time()
    logging.debug("Started Searching")
    # validating that the input is right types
    if not isinstance(SearchQuery, dict):
        logging.error(f"SearchQuery must be a dict; got: {type(SearchQuery)}")
        raise ValueError("RecipeID must be an dict.")

    if not isinstance(RecipesClass, list):
        logging.error(f"RecipesClass must be a list; got: {type(RecipesClass)}")
        raise ValueError("RecipeID must be an list.")

    if not isinstance(RecipeKeys, dict):
        logging.error(f"RecipeKeys must be a dict; got: {type(RecipeKeys)}")
        raise ValueError("RecipeID must be an dict.")

    # 1
    # validating that all the input of the SearchQuery to check if they all contain the right info and if we can skip searches
    SearchTypes = _findPossibleSearch(SearchQuery, getPossibleSearchTypes())

    # 2
    # grab the list now for what search types exists and sends it to be searched, give ing a set of recipes names
    result = []
    for searchType in SearchTypes:
        for searchQuery in SearchQuery[searchType]:
            result.append(_searchRecepy(RecipesClass, searchType, searchQuery))
            logging.debug(f"Results: {result}")

    # 3
    # getting a set of all recipe id's

    Result = set()
    for x in result:
        if len(x) == 0:
            logging.debug(f"Contained nothing, next set")
            continue

        Result = x.union(Result)
        logging.debug(f"All valid recipe IDs {Result}, Last union: {x}")

    Result = sorted(list(Result))
    logging.debug(f"Search Result: {Result}")
    logging.debug(f"time taken: {time.time()-StartTime}")
    return Result


def _searchRecepy(RecipesClass, searchType, searchQuery) -> set:

    logging.debug(f"searching for type: {searchType}, query: {searchQuery}")

    match searchType:
        case "Text":
            return _TextSearchType(RecipesClass, searchQuery)

        case "Ingredient":
            return _IngredientSearchType(RecipesClass, searchQuery)

        case "Equipment":
            return set()
            
        case "Allergen":
            return set()

def _IngredientSearchType(RecipesClass, searchQuery) -> set:
    ValidSearchedRecipes = set()

    for Recipe in RecipesClass:
        Ingredients = Recipe.Get_Ingredients()
        logging.debug(f"on: {Recipe.get_name()}")

        # checking if the recipe has any ingredient
        if len(Ingredients) == 0:
            logging.debug(f"{Recipe.get_name()} dose not have any ingredient, skipped")
            continue


        for IngredientObj in Ingredients:
            Ingredient = IngredientObj.getIngredient()
            logging.debug(f"Scanning if ingredient: {Ingredient.lower()} is to {searchQuery.lower()}")
            if Ingredient.lower() == searchQuery.lower():
                logging.debug(f"Found match: {Ingredient}")
                ValidSearchedRecipes.add(Recipe.get_recipe_id())
                break
            else:
                logging.debug(f"Not true")

    return ValidSearchedRecipes


def _TextSearchType(RecipesClass, searchQuery) -> set:
    ValidSearchedRecipes = set()

    for Recipe in RecipesClass:
        RecipeName = Recipe.get_name()
        logging.debug(f"Scanning if recipe: {RecipeName.lower()} is to {searchQuery.lower()}")

        if searchQuery.lower() in RecipeName.lower():
            logging.debug(f"Found {RecipeName.lower()}")
            ValidSearchedRecipes.add(Recipe.get_recipe_id())

        else:
            logging.debug(f"Not true")

    return ValidSearchedRecipes

def _findPossibleSearch(SearchQuery, PossibleSearchTypes) -> list:
    SearchTypes = set()

    # go thr the SearchQuery keys, match it with the SearchTypesCalls keys and if true increment the SearchTypesCalls value
    for key in SearchQuery:

        if key not in PossibleSearchTypes:
            logging.error(f"Search query contains a key that was not expected; got: {key}, needed to be {PossibleSearchTypes}")
            raise ValueError

        SearchTypes.add(key)

    logging.debug(f"All possible calls and reductions: {SearchTypes}")

    return list(SearchTypes)


def getPossibleSearchTypes() -> list:
    return ["Text", "Ingredient", "Equipment", "Allergen"]