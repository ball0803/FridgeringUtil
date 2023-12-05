import json
import requests
from tqdm import tqdm

with open('ingredients_process.json') as f:
    data = json.load(f)

url = 'https://fridgeringapi.fly.dev/common_ingredient'
start_index = 0


# Read the start index from the file
try:
    with open('index.txt', 'r') as f:
        start_index = int(f.read())
except FileNotFoundError:
    pass

# Loop over each item in data['FoundationFoods'], starting from start_index
for i in tqdm(range(start_index, len(data)), desc='Posting data'):
    doc = data[i]
    payload = {
        "description": doc.get("description"),
        "foodNutritients": doc.get("foodNutrients"),
        "foodAttributes": doc.get("foodAttributes"),
        "fdcId": doc.get("fdcId"),
        "inputFoods": doc.get("inputFoods"),
        "foodPortions": doc.get("foodPortions"),
        "foodCategory": doc.get("foodCategory") or doc.get("wweiaFoodCategory"),
        "ndbNumber": doc.get("ndbNumber") or doc.get("fdcId"),
        "image": doc.get("image")
    }
    json_payload = json.dumps(payload)
    # print(json_payload)

    response = requests.post(url, data=json_payload, headers={'Content-Type': 'application/json'})
    print(response.text)

    # If the POST request was successful, save the current index to the file
    while response.status_code != 200:
        response = requests.post(url, data=json_payload, headers={'Content-Type': 'application/json'})
        print(response.text)
        # print(payload)
    if response.status_code == 200:
        with open('index.txt', 'w') as f:
            f.write(str(i))