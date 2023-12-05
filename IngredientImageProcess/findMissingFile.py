import json
import shutil
import os

with open('ingredients_process1.json', 'r') as f:
    ingredients = json.load(f)

missing = []
for ingredient in ingredients:
    if 'image' not in ingredient:
        missing.append(ingredient['description'])

missing = [name.replace('/', '-').replace('"', '-').replace(':', '-')[:200] + '.png' for name in missing]  # append .png here

path1 = "C:\\Users\\COMPUTER\\Desktop\\Ingredient Image"
path2 = "C:\\Users\\COMPUTER\\Desktop\\missing"

for file_name in missing:
    source = os.path.join(path1, file_name)
    destination = os.path.join(path2, file_name)
    if os.path.exists(source):
        shutil.copy2(source, destination)

print(missing)