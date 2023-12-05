import requests
import json

with open('deleteFdc.txt', 'r') as f:
    delete_fdcIds = [line.strip() for line in f]

for fdcId in delete_fdcIds:
    # print(fdcId)
    url = f'https://fridgeringapi.fly.dev/common_ingredient/{fdcId}'
    response = requests.delete(url)
    print(response.status_code)
    print(response.text)
    print()