import re
from googletrans import Translator
import json
from tqdm import tqdm

def preprocess_ingredient(ingredient):
    # Define a list of possible units
    units = ['cup', 'cups', 'tbsp', 'tsp', 'ounce', 'oz', 'g', 'cc', 'gram', 'kg', 'pound', 'lb', 'ea', 'pcs', 'ml', 'L', 'gallon', 'handful', 'splash', 'pinch', 'drop', 'package', 'can', 'jar', 'bottle', 'bunch', 'root', 'clove', 'slice', 'head', 'dash', 'sprig', 'potion', 'ladle', 'portion', 'cm', 'to-taste', 'mg']

    # Initialize variables for the amount, unit, and ingredient name
    amount = None
    unit = None
    ingredient_name = ingredient.lower()

    if 'to-taste' in ingredient.lower():
        parts = ingredient.lower().split('to-taste', 1)
        amount = 'to-taste'
        # print(parts)
        unit = None
        ingredient_name = ''.join(parts).strip()
    # Check if the ingredient contains a unit
    else:
        last_word = ingredient_name.split()[-1]
        if last_word in units:
            # Check if the word before the last word is a number
            second_last_word = ingredient_name.split()[-2]
            if second_last_word.isdigit() or '-' in second_last_word or '/' in second_last_word:
                # Set the last word as the unit, the word before it as the amount, and the rest as the ingredient name
                unit = last_word
                amount = second_last_word
                ingredient_name = ' '.join(ingredient_name.split()[:-2]).strip()
        else:
            for possible_unit in units:
                if re.search(fr'\b{possible_unit}\b', ingredient_name):
                    parts = re.split(fr'\b{possible_unit}\b', ingredient_name, 1)
                    amount = parts[0].strip()
                    ingredient_name = parts[1].strip()

                    unit = possible_unit
                    break

        # If the ingredient does not contain a unit, check if it contains a number at the beginning or end
        if not unit:
            amount_and_unit_match = re.search(r'(\d+\.?\d*|\d*\.?\d+|\d+-\d+)([a-zA-Z]*)', ingredient_name)
            if amount_and_unit_match:
                amount = amount_and_unit_match.group(1)
                unit = amount_and_unit_match.group(2)
                ingredient_name = re.sub(fr'\b{amount}{unit}\b', '', ingredient_name).strip()

        # If the amount is a range like "1-2", separate it from the ingredient name
        if '-' in str(amount) and len(amount.split(' ')) > 1:
            ingredient_name = amount.split(' ')[0]
            amount = amount.split(' ')[1]

    return amount, unit, ingredient_name.strip()

def extract_possible_units(ingredients):
    units = set()

    for ingredient in ingredients:
        # Define a regex pattern to extract numeric values and units (including Thai, English, and ".")
        pattern = r'(\d+(\.\d+)?)\s*([ก-๙a-zA-Z.]+)\b'

        # Find all matches in the ingredient
        matches = re.findall(pattern, ingredient)

        # Collect unique units
        for match in matches:
            _, _, unit = match
            units.add(unit)

    return list(units)

    
# print(translate_ingredients, ingredients)

with open('preprocessed_recipes.json', 'r', encoding='utf-8') as f:
    recipes = json.load(f)

# for recipes in recipes[:2]:
#     ingredients = recipes['ingredients']
translator = Translator()
#     translate_ingredients = []
#     for ingredient in ingredients:
#         translate_ingredients.append(translator.translate(ingredient, dest='en').text)
#     print(translate_ingredients)

# possible_units = extract_possible_units(ingredients)
# print("Possible Units:", possible_units)

for recipe in tqdm(recipes, desc="Processing recipes"):
    ingredients = recipe['ingredients']
    # print(recipe)
    ingredient_cols = []

    if 'ingredients_collection' in recipe:
        # If the number of items in 'ingredients_collection' is equal to the number of 'ingredients', skip this iteration
        if len(recipe['ingredients_collection']) == len(ingredients):
            continue
        # If the number of items in 'ingredients_collection' is not equal to the number of 'ingredients', start from the last element of 'ingredients_collection'
        else:
            start_index = len(recipe['ingredients_collection'])
            ingredients = ingredients[start_index:]

    for ingredient in ingredients:
        ingredient = translator.translate(ingredient, dest='en', src='th').text
        # print(ingredient)
        amount, unit, text = preprocess_ingredient(ingredient)
        ingredient_cols.append({"amount": amount, "unit": unit, "name": text})
        # print(f"Amount: {amount}, Unit: {unit}, Ingredient: {text}")
    recipe['ingredients_collection'] = ingredient_cols

    with open('preprocessed_recipes.json', 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=4)

