
def AddExtraIngredient():

    """
    Add one or more extra ingredients to the already made ingredient database.

    Prompts the user for the ingredient name and category, checks whether
    the ingredient already exists, generates a new ID, and saves the
    ingredient to ingredients.json.

    Parameters:
        None

    Returns:
        None
    """
   
    with open ('ingredients.json','r') as file:   #open json file that contains our Ingredients in read mode
        Ingredients_known= json.load(file) 

    Ingredients_num= int(input("How many ingredients do you want to add? ")) # get ingredients number
    for i in range(Ingredients_num): # just a loop to get Ingredient name and category (may change category part later)
        Ingredient_name = input("Input ingredient name: ")
        Ingredient_category = input("Input ingredient category: ")

    for products in Ingredients_known["product"].values(): # Product is the name of the list in json file that contains the dictionary ID of the Veggies and fruits
        if products["name"].casefold()==Ingredient_name.casefold: # compare values in json file and the one written in the dictionary if yes then go to print if no then add to list of ingredeints
            print("Ingredient already exists")
            break

    New_ID = str(max(map(int, Ingredients_known["product"].keys()), default=0) + 1) #assigns new id to ingredients we don't know

            # Add the ingredient
    Ingredients_known["product"][New_ID] = {
                "name": Ingredient_name,
                "category": Ingredient_category
            }
        
    with open ('ingredients.json','w') as file:
                json.dump(Ingredients_known, file, indent=2) # add the ingredient in json file

AddExtraIngredient()



