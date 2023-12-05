import json
import requests
from tqdm import tqdm
import time

url = 'http://localhost:3000/recipes'
start_index = 0

try:
    with open('index.txt', 'r') as f:
        start_index = int(f.read())
except FileNotFoundError:
    pass

with open('last_recipes.json', 'r', encoding="utf-8") as f:
    recipes = json.load(f)

for i in tqdm(range(start_index, len(recipes)), desc='Posting data'):
    recipe = recipes[i]
    payload = {
        'name': recipe['header'],
        'image': recipe['img_urls'],
        'cookTime': recipe['cookTime'],
        'prepTime': recipe['prepTime'],
        'url': recipe['url'],
        'instructions': recipe['instructions'],
        'ingredients': recipe['ingredients_collection'],
        'tags': recipe['tags']
    }
    json_payload = json.dumps(payload)

    response = requests.post(url, data=json_payload, headers={'Content-Type': 'application/json'})

    # # If the POST request was successful, save the current index to the file
    while response.status_code != 200:
        time.sleep(1)
        response = requests.post(url, data=json_payload, headers={'Content-Type': 'application/json'})
        print(response.text)

    # If the POST request was successful, save the current index to the file
    if response.status_code == 200:
        with open('index.txt', 'w') as f:
            f.write(str(i))