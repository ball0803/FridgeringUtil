
import json
import requests
from tqdm import tqdm

with open('srFood.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url = 'http://localhost:8080/add_common_ingredient'
start_index = 0

# Read the start index from the file
try:
    with open('index.txt', 'r') as f:
        start_index = int(f.read())
except FileNotFoundError:
    pass

# Loop over each item in data['FoundationFoods'], starting from start_index
for i in tqdm(range(start_index, len(data['SRLegacyFoods'])), desc='Posting data'):
    doc = data['SRLegacyFoods'][i]
    payload = {
        "description": doc.get("description"),
        "foodNutritients": doc.get("foodNutrients"),
        "foodAttributes": doc.get("foodAttributes"),
        "fdcId": doc.get("fdcId"),
        "inputFoods": doc.get("inputFoods"),
        "foodPortions": doc.get("foodPortions"),
        "foodCategory": doc.get("foodCategory"),
        "ndbNumber": doc.get("ndbNumber")
    }
    json_payload = json.dumps(payload)
    # print(json_payload)

    response = requests.post(url, data=json_payload, headers={'Content-Type': 'application/json'})
    # print(response)

    # If the POST request was successful, save the current index to the file
    if response.status_code == 200:
        with open('index.txt', 'w') as f:
            f.write(str(i))