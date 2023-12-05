import json
import requests
from tqdm import tqdm
import time

with open('ingredients_process.json', 'r') as f:
    ingredients = json.load(f)

count = 0

for ingredient in tqdm(ingredients):
    fdcIds = ingredient['fdcId']
    path = f"https://fridgeringapi.fly.dev/common_ingredient/{fdcIds}"
    response = requests.get(path)
    if response.status_code == 200:
        print(response.text)
    else:
        count += 1
        print(path)
        print(response.status_code, response.text)
        print(ingredient['description'], ingredient['image'], ingredient['fdcId'])

    # Sleep for 1 second to avoid rate limiting
    time.sleep(1)

# print(count)
