import logging
import time
from concurrent.futures import ThreadPoolExecutor
import time

def searchRecipes(SearchQuery, RecipesClass) -> list:
    """
    Searches thru a database to get recipes that follow citrin patters

    Parameters:
    SearchQuery (dict): a dict where
        key: the type of search (getPossibleSearchTypes())
        value: an array of all search queuers that should be preformed with that search
    RecipesClass (list): A OOP list of every recipe stored inside of the DB

    Returns:
    list: a list of RecipesID (which are inside of the RecipesClass) with the i[0] being the most likely result and i[-1] being the least likely
    """
    StartTime = time.time()
    logging.info(f"Started Searching, Query: {SearchQuery}")

    # 0
    # validating that the input is right types
    if not isinstance(SearchQuery, dict):
        logging.error(f"SearchQuery must be a dict; got: {type(SearchQuery)}")
        raise ValueError("RecipeID must be an dict.")

    if not isinstance(RecipesClass, list):
        logging.error(f"RecipesClass must be a list; got: {type(RecipesClass)}")
        raise ValueError("RecipeID must be an list.")

    # 1
    # validating that all the input of the SearchQuery to check if they all contain the right info and if we can skip searches
    SearchTypes = _findPossibleSearch(SearchQuery, getPossibleSearchTypes())

    # 2
    # grab the list now for what search types exists and sends it to be searched, give ing a set of recipes names

    Results = []
    for searchType in SearchTypes:
        for searchQuery in SearchQuery[searchType]:
            Results.append(_searchIndividualQuery(RecipesClass, searchType, searchQuery))
            logging.debug(f"Results: {Results}")

    
    # multiline test, this code works, I dont know if its faster since the DB is to small, this is for the future, but currently its slower
    """
    Results = []
    with ThreadPoolExecutor() as executor:
        for searchType in SearchTypes:
            for searchQuery in SearchQuery[searchType]:
                Results.append(executor.submit(_searchIndividualQuery, RecipesClass, searchType, searchQuery))

    Results = [future.result() for future in Results]
    """

    # 3
    # sorting the ID's by most possible recipe (e.g, the more requirements it satisfies the high on the list it is)

    WeightedResults = dict()
    for Values in Results:
        if len(Values) == 0:
            logging.debug(f"Contained nothing, next set")
            continue

        for PossibleResult in Values:
            # if the result was not yet inside of a dict
            if PossibleResult not in WeightedResults:
                WeightedResults[PossibleResult] = 1
                logging.debug(f"First element for recipe ID: {PossibleResult}: #{WeightedResults[PossibleResult]}")
            else:
                WeightedResults[PossibleResult] += 1
                logging.debug(f"Added element for recipe ID: {PossibleResult}: #{WeightedResults[PossibleResult]}")

    logging.debug(f"Weighted results are: {WeightedResults}")

    # 4
    # convert the list of elements into a flat array
    SearchResults = []
    while WeightedResults:
        HighestKey = max(WeightedResults, key=lambda key: WeightedResults[key])
        WeightedResults.pop(HighestKey)
        SearchResults.append(HighestKey)

    logging.info(f"Search ended")
    logging.info(f"Time: {time.time()-StartTime}")
    logging.info(f"Search Results: {SearchResults}")
    return SearchResults
            


def _searchIndividualQuery(RecipesClass, searchType, SearchQuery) -> set:

    logging.debug(f"searching for type: {searchType}, query: {SearchQuery}")

    match searchType:
        case "Text":
            return _textSearchType(RecipesClass, SearchQuery)

        case "Ingredient":
            return _ingredientSearchType(RecipesClass, SearchQuery)

        case "Equipment":
            return _equipmentSearchType(RecipesClass, SearchQuery)
            
        case "Allergen":
            return _allergenSearchType(RecipesClass, SearchQuery)

    logging.error(f"Search Type: {searchType} dose not exists, returned an empty result to just continue the code, but search result will not be as accurate as expected")
    return set()

def _allergenSearchType(RecipesClass, SearchQuery) -> set:
    ValidSearchedRecipes = set()

    for Recipes in RecipesClass:
        Allergens = Recipes.get_Allergies()
        logging.debug(f"on {Recipes.get_name()}")

        if len(Allergens) == 0:
            logging.debug(f"on {Recipes.get_name()} dose not have any allergens")

        logging.debug(f"Checking if {SearchQuery} dose not contain {Allergens}")
        if SearchQuery.lower() not in [Item.lower() for Item in Allergens]:
            logging.debug(f"No match found")
            ValidSearchedRecipes.add(Recipes.get_recipe_id())



    return ValidSearchedRecipes

def _equipmentSearchType(RecipesClass, SearchQuery) -> set:
    ValidSearchedRecipes = set()

    for Recipe in RecipesClass:
        Equipments = Recipe.get_Equipment()
        logging.debug(f"on: {Recipe.get_name()}")

        if len(Equipments) == 0:
            logging.debug(f"{Recipe.get_name()} dose not have any equipment")

        logging.debug(f"scanning if {Equipments} is equal to {SearchQuery}")

        if SearchQuery.lower() in [Item.lower() for Item in Equipments]:
            logging.debug(f"match found")
            ValidSearchedRecipes.add(Recipe.get_recipe_id())

    return ValidSearchedRecipes


def _ingredientSearchType(RecipesClass, SearchQuery) -> set:
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
            logging.debug(f"Scanning if ingredient: {Ingredient.lower()} is to {SearchQuery.lower()}")
            if Ingredient.lower() == SearchQuery.lower():
                logging.debug(f"Found match: {Ingredient}")
                ValidSearchedRecipes.add(Recipe.get_recipe_id())
                break

    return ValidSearchedRecipes


def _textSearchType(RecipesClass, SearchQuery) -> set:
    ValidSearchedRecipes = set()

    for Recipe in RecipesClass:
        RecipeName = Recipe.get_name()
        logging.debug(f"Scanning if recipe: {RecipeName.lower()} is to {SearchQuery.lower()}")

        if SearchQuery.lower() in RecipeName.lower():
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