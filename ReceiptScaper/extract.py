import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import json
from tqdm import tqdm

options = uc.ChromeOptions() 
options.headless = False 
driver = uc.Chrome(use_subprocess=True, options=options) 

with open('Web Development\Receipt scaper\links.txt', 'r') as f:
    urls = f.readlines()

recipes = []
try:
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)

except FileNotFoundError:
    pass

for url in tqdm(urls, desc="Scraping recipes"):
    url = url.strip()
    if any(recipe['url'] == url for recipe in recipes):
        continue

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    inner_text = '|'.join(soup.stripped_strings)

    tag_pattern = r'แท็ก[\S\s]*(?=เผยแพร่)'
    instruction_pattern = r'วิธีทำ(?!โดย)[\s\S]*(?=แท็ก)'
    ingredient_pattern = r'(?:วัตถุดิบ|ส่วนผสม)(?:(?!วิธีทำ).)*'

    header = soup('h1')[0].text
    tag_match = re.search(tag_pattern, inner_text)
    instruction_match = re.search(instruction_pattern, inner_text)
    ingredient_match = re.search(ingredient_pattern, inner_text)

    img_elements = driver.find_elements(By.CSS_SELECTOR, ".slick-track img")
    if not img_elements:
        img_elements = driver.find_elements(By.CSS_SELECTOR, ".epawmp-0 img")
    img_urls = list(set([img.get_attribute("src") for img in img_elements]))

    instruction =  [r.strip() for r in instruction_match.group().split('|') if r.strip()]
    ingredient = [r.strip() for r in ingredient_match.group().split('|') if r.strip()]
    new_ingredient = []
    new_instuction = []
    tag_match = [ r.strip() for r in tag_match.group().split('|') if r.strip()]
    tag_match.pop(0)

    if len(ingredient) % 2 != 0:
        new_ingredient.append(ingredient[0])
        for i in range(1, len(ingredient), 2):
            new_ingredient.append(ingredient[i] + " " + ingredient[i+1])
    else:
        for i in range(0, len(ingredient), 2):
            new_ingredient.append(ingredient[i] + " " + ingredient[i+1])

    # print(instruction)
    for i in range(len(instruction)):
        if instruction[i].startswith('STEP') or instruction[i] == "1":
            new_instuction.append(' '.join(instruction[:i+1]))
            for j in range(i, len(instruction)):
                if instruction[j-1].isnumeric():
                    # print(instruction[j-1] + " " + instruction[j])
                    new_instuction.append(instruction[j-1] + " " + instruction[j])
                elif not instruction[j].isnumeric():
                    # print(instruction[j])
                    new_instuction.append(instruction[j])
            # for j in range(i, len(instruction), 2):
            #     print(instruction[j] + " " + instruction[j+1])
                # new_instuction.append(instruction[j] + " " + instruction[j+1])
            break

    recipe = {
        'url': url,
        'header': header,
        'img_urls': img_urls,
        'ingredients': new_ingredient,
        'instructions': new_instuction,
        'tag': tag_match
    }
    recipes.append(recipe)

    # Write the recipe information to a JSON file after scraping each URL
    with open('recipes.json', 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=4)

driver.quit()