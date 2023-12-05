from fuzzywuzzy import process
import json
from tqdm import tqdm


def fuzzy_search(search_term, string_array):
    # Use process.extractOne to find the most similar string
    result, score = process.extractOne(search_term, string_array)

    # Find the index of the most similar ingredient
    index = next(i for i, ingredient in enumerate(ingredients) if ingredient['description'] == result)

    return result, score, index

# Open and load the JSON file
with open('./asset/ingredients_process.json') as f:
    ingredients = json.load(f)

with open('last_recipes.json', 'r', encoding='utf-8') as f:
    recipes = json.load(f)


descriptions = [ingredient['description'] for ingredient in ingredients]
for recipe in tqdm(recipes, desc="Processing recipes"):
    ingredient_cols = recipe['ingredients_collection']
    for ingredient in ingredient_cols:
        if 'ndbNumber' in ingredient or ingredient['name'].strip() == '' or ingredient['name'].strip() == '.':
            continue
        # print(ingredient['name'])
        # Separate the ingredients into two arrays
        # ndbNumbers = [ingredient['ndbNumber'] for ingredient in ingredients]

        search_result, similarity_score, index = fuzzy_search(ingredient['name'], descriptions)
        # print(f"Result: {search_result}, Similarity Scoe: {similarity_score}, Index: {index}")
        ingredient['common_name'] = search_result
        ingredient['fcdId'] = ingredients[index]['fdcId']
        # ingredient['ndbNumber'] = ingredients[index]['ndbNumber']
        # print(f"Corresponding ingredients: {json.dumps(ingredients[index], indent=4)}")

    # print(ingredient_cols)
with open('last_recipes.json', 'w', encoding='utf-8') as f:
    json.dump(recipes, f, ensure_ascii=False, indent=4)