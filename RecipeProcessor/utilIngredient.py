import json
from tqdm import tqdm

with open('./asset/ingredients_process.json', 'r', encoding='utf-8') as f:
    ingredients = json.load(f)

with open('descriptions.txt', 'w', encoding='utf-8') as f:
    for ingredient in tqdm(ingredients):
        f.write(ingredient['description'] + '\n')