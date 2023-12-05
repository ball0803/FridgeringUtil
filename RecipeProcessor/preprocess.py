import json
import re
from tqdm import tqdm

with open('progress.json', 'r', encoding='utf-8') as f:
    recipes = json.load(f)['recipes']
# with open('recipes.json', 'r', encoding='utf-8') as f:
#     recipes = json.load(f)

with open('unitConverter.json', 'r', encoding='utf-8') as f:
    data = json.load(f)['data']

check_strings = ["ส่วนผสม", "สำหรับ", "ถูกใจ", "วัตถุดิบ", "ความคิดเห็น"]

for recipe in recipes:
    # Create a new list of ingredients that do not contain the strings
    recipe['ingredients'] = [ingredient for ingredient in recipe['ingredients'] if not any(string in ingredient for string in check_strings)]

replace_strings = {"½": "1/2", "ประมาณ": "", " แล้วแต่ชอบ": " to-taste", " ตามชอบ": " to-taste", " แล้วแต่": " to-taste", "แล้วแต่ชอบ ": "to-taste ", "ตามชอบ ": "to-taste ", "แล้วแต่ ": " to-taste ", " ครึ่งช้อน": " 1/2 tbsp"}

for recipe in recipes:
    ingredients = recipe['ingredients']
    for i, ingredient in enumerate(ingredients):
        # Replace each string in replace_strings from the ingredient
        for string, replacement in replace_strings.items():
            ingredient = ingredient.replace(string, replacement)
        # Update the ingredient in the recipe
        ingredients[i] = ingredient


# Replace units in the string
units_and_names = sorted([(unit, name) for unit, names in data.items() for name in names], key=lambda x: len(x[1]), reverse=True)

for recipe in tqdm(recipes, desc="Processing recipes"):
    ingredients = recipe['ingredients']
    for i, ingredient in enumerate(ingredients):
        parts = ingredient.split()
        for j, part in enumerate(parts):
            if re.search(r'\d', part) and re.search(r'[^\d/.-]', part):
                # Separate the number from the character
                number = re.search(r'\d+', part).group()
                character = re.search(r'[^\d/.-]+', part).group()
                parts[j] = number + ' ' + character
        # Join the parts back together
        ingredient = ' '.join(parts)
        for unit, name in units_and_names:
            # Use a regular expression to replace the unit only when it appears as a whole word
            ingredient = re.sub(r'(\d+)\s*\b' + re.escape(name) + r'\b', r'\1 ' + unit, ingredient)
        # Update the ingredient in the recipe
        ingredients[i] = ingredient

# Save the modified recipes to a new file
with open('preprocessed.json', 'w', encoding='utf-8') as f:
    json.dump(recipes, f, ensure_ascii=False, indent=4)