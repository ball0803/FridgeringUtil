import json

with open("survey_food.json", "r") as f:
    data = json.load(f)

data = data["SurveyFoods"]
print(data[1].keys())