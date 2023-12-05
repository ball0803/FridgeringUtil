from fuzzywuzzy import fuzz
import json
from tqdm import tqdm

# Load the ingredients from the file
with open('./asset/ingredients.json', 'r') as f:
    ingredients = json.load(f)

# Create a list to store the unique ingredients
unique_ingredients = []

for ingredient in tqdm(ingredients):
    # print(ingredient)
    # If the unique_ingredients list is empty, add the first ingredient
    if not unique_ingredients:
        # print(ingredient)
        unique_ingredients.append(ingredient)
    else:
        # Compare the ingredient to the unique ingredients
        # If it's not similar to any of them, add it to the list
        if not any(fuzz.ratio(ingredient["description"], unique_ingredient["description"]) > 70 for unique_ingredient in unique_ingredients):
            unique_ingredients.append(ingredient)

# Write the unique ingredients back to the file
with open('./asset/ingredients_process.json', 'w') as f:
    json.dump(unique_ingredients, f)