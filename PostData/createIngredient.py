import json
from tqdm import tqdm

with open('foundation.json', 'r', encoding='utf-8') as f:
    data1 = json.load(f)

with open('srFood.json', 'r', encoding='utf-8') as f:
    data2 = json.load(f)

with open('survey_food.json', 'r', encoding='utf-8') as f:
    data3 = json.load(f)

ingredients = []

for ingredient in tqdm(data1['FoundationFoods']):
    payload = {
        "description": ingredient["description"],
        "foodNutritients": ingredient["foodNutrients"],
        "foodAttributes": ingredient["foodAttributes"],
        "fdcId": ingredient["fdcId"],
        "inputFoods": ingredient["inputFoods"],
        "foodPortions": ingredient["foodPortions"],
        "foodCategory": ingredient["foodCategory"],
        "ndbNumber": ingredient["ndbNumber"]
    }
    ingredients.append(ingredient)

for ingredient in tqdm(data2['SRLegacyFoods']):
    payload = {
        "description": ingredient["description"],
        "foodNutritients": ingredient["foodNutrients"],
        "foodAttributes": ingredient["foodAttributes"],
        "fdcId": ingredient["fdcId"],
        "inputFoods": ingredient["inputFoods"],
        "foodPortions": ingredient["foodPortions"],
        "foodCategory": ingredient["foodCategory"],
        "ndbNumber": ingredient["ndbNumber"]
    }
    ingredients.append(ingredient)

for ingredient in tqdm(data3['SurveyFoods']):
    payload = {
        "description": ingredient["description"],
        "foodNutritients": ingredient["foodNutrients"],
        "foodAttributes": ingredient["foodAttributes"],
        "fdcId": ingredient["fdcId"],
        "inputFoods": ingredient["inputFoods"],
        "foodPortions": ingredient["foodPortions"],
        "foodCategory": ingredient["wweiaFoodCategory"],
        "ndbNumber": ingredient["fdcId"]
    }
    ingredients.append(ingredient)

with open('ingredients.json', 'w') as f:
    json.dump(ingredients, f, indent=4)