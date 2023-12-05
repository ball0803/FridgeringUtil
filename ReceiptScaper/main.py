from zenrows import ZenRowsClient
import re
from bs4 import BeautifulSoup

# Create a BeautifulSoup object to parse the HTML

# Extract the inner text from the parsed HTML
client = ZenRowsClient("c80d18ac8d0eae67ef8f5d4f1903a8a0eef54cd2")
url = "https://www.wongnai.com/recipes/ugc/71f45d802d2a43cd813f66ea242cce26"

response = client.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
inner_text = '|'.join(soup.stripped_strings)
instruction_pattern = r'วิธีทำ(?!โดย)(?:(?:(?!วิธี|แท็ก).)*?(?:\b(?:STEP|\d+)\b(?:.*?))?)+.*?(?=แท็ก)'
ingredient_pattern = r'(?:วัตถุดิบ|ส่วนผสม)(?:(?!วิธีทำ).)*'

header = soup('h1')[0].text
instruction_match = re.search(instruction_pattern, inner_text)
ingredient_match = re.search(ingredient_pattern, inner_text)

# print(response.text)
# print(inner_text)
# print(header)
print(instruction_match.group())
# print(ingredient_match.group().split('|'))
instruction =  [r.strip() for r in instruction_match.group().split('|') if r.strip()]
ingredient = [r.strip() for r in ingredient_match.group().split('|') if r.strip()]
new_list = []

for i in range(0, len(ingredient), 2):
    new_list.append(ingredient[i] + " " + ingredient[i+1])

print(new_list)
new_instuction = []
for i in range(len(instruction)):
    if instruction[i].startswith('STEP') or instruction[i].startswith('1'):
        new_instuction.append(' '.join(instruction[:i+1]))
        for j in range(i+1, len(instruction), 2):
            new_instuction.append(instruction[j] + " " + instruction[j+1])
        break

print(new_instuction)