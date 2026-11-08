import logging

def searchRecipes(SearchQuery, RecipesClass, RecipeKeys) -> list:

    print(SearchQuery)

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
    for searchType in SearchTypes:
        for searchQuery in SearchQuery[searchType]:
            text = _searchRecepy(RecipesClass, searchType, searchQuery)
            print(text)



    return []

def _searchRecepy(RecipesClass, searchType, searchQuery) -> set:

    logging.debug(f"searching for type: {searchType}, query: {searchQuery}")

    match searchType:
        case "Text":
            return(_TextSearchType(RecipesClass, searchQuery))

        case "Ingredient":
            return set()

        case "Equipment":
            return set()
            
        case "Allergen":
            return set()
            

def _TextSearchType(RecipesClass, searchQuery) -> set:
    ValidSearchedRecipes = set()

    for recipe in RecipesClass:
        recipeName = recipe.get_name()

        if searchQuery.lower() in recipeName.lower():
            ValidSearchedRecipes.add(recipeName)

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