import re
import json
from tqdm import tqdm

with open('last_recipes.json', 'r', encoding='utf-8') as f:
    recipes = json.load(f)

# with open('last_recipes3.json', 'r', encoding='utf-8') as f:
#     recipes2 = json.load(f)

# for recipe in tqdm(recipes, desc="Processing recipes"):
#     instructions = recipe['instructions']
#     if instructions[0].startswith("วิธีทำ"):
#         prep_time_matches = re.findall(r'เวลาเตรียมส่วนผสม: (\d+) ชั่วโมง (\d+) นาที', instructions[0])
#         prep_time_matches_min = re.findall(r'เวลาเตรียมส่วนผสม: (\d+) นาที', instructions[0])
#         cook_time_matches = re.findall(r'เวลาปรุงอาหาร: (\d+) ชั่วโมง (\d+) นาที', instructions[0])
#         cook_time_matches_min = re.findall(r'เวลาปรุงอาหาร: (\d+) นาที', instructions[0])
#         prep_time = 0
#         cook_time = 0
        
#         if prep_time_matches:
#             prep_time_hours = int(prep_time_matches[0][0])
#             prep_time_minutes = int(prep_time_matches[0][1])
#             prep_time = prep_time_hours * 60 + prep_time_minutes
#             # print(f"Preparation time: {prep_time_hours} hours and {prep_time_minutes} minutes")
        
#         elif prep_time_matches_min:
#             prep_time_minutes = int(prep_time_matches_min[0])
#             prep_time = prep_time_minutes
#             # print(f"Preparation time: {prep_time_minutes} minutes")
        
#         if cook_time_matches:
#             cook_time_hours = int(cook_time_matches[0][0])
#             cook_time_minutes = int(cook_time_matches[0][1])
#             cook_time = cook_time_hours * 60 + cook_time_minutes
#             # print(f"Cooking time: {cook_time_hours} hours and {cook_time_minutes} minutes")
        
#         elif cook_time_matches_min:
#             cook_time_minutes = int(cook_time_matches_min[0])
#             cook_time = cook_time_minutes
#             # print(f"Cooking time: {cook_time_minutes} minutes")
        
#         recipe['prepTime'] = prep_time
#         recipe['cookTime'] = cook_time
#         instructions.pop(0)

# for recipe in tqdm(recipes):
#     instructions = recipe['instructions']
#     if instructions[0].startswith("1 วิธีทำ"):
#         instructions[0] = instructions[0].replace("1 วิธีทำ", "")


# for recipe in tqdm(recipes):
#     instruction = recipe['instructions']
#     if len(instruction) == 1:
#         # print(instruction)
#         split_instructions = re.split(r'(\d+\.?.+?(?=\n\d+\.?|$))', instruction[0])
#         split_instructions = [instr.strip() for instr in split_instructions if instr.strip()]
#         # print(split_instructions)
#         recipe['instructions'] = split_instructions

# for recipe in tqdm(recipes):
#     instructions = recipe['instructions']
#     for i in range(len(instructions)):
#         # print(instructions[i])
#         instructions[i] = re.sub(r'^(\d+)\s+\1\.', r'\1.', instructions[i])
#         # print(instructions[i])

# for idx, recipe in tqdm(enumerate(recipes)):
#     recipe2 = recipes2[idx]
#     recipe['instructions'] = recipe2['instructions']

# for recipe in tqdm(recipes):
#     for ingredient in recipe['ingredients_collection']:
#         if 'common_name' in ingredient:
#             del ingredient['common_name']
#         if 'fcdId' in ingredient:
#             del ingredient['fcdId']
    
with open('last_recipes.json', 'w', encoding='utf-8') as f:
    json.dump(recipes, f, ensure_ascii=False, indent=4)