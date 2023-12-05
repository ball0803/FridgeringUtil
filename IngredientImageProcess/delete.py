import json

with open('ingredients_process.json', 'r') as f:
    ingredients = json.load(f)

with open('delete.txt', 'r') as f:
    delete = [line.strip() for line in f]

delete_fdcIds = []
# print(delete)
for ingredient in ingredients:
    if ingredient['description'] in delete:
        print(ingredient['description'])
        ingredients.remove(ingredient)
# ingredients = [ingredient for ingredient in ingredients if not any(word in ingredient['description'] for word in delete) or delete_fdcIds.append(str(ingredient['fdcId'])) is None]

# with open('deleteFdc.txt', 'w') as f:
#     for fdcId in delete_fdcIds:
#         f.write(fdcId + '\n')

# with open('ingredients_process.json', 'w') as f:
#     json.dump(ingredients, f, indent=4)