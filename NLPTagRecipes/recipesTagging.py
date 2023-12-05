import spacy
from googletrans import Translator
# from translate import Translator
import json
from tqdm import tqdm
import multiprocessing

nlp = spacy.load('en_core_web_md')

def find_similar_tags(text, existing_tags, threshold=0.5):
    doc = nlp(text)
    keywords = [token.text for token in doc if not token.is_stop]

    similar_tags = []

    for keyword in tqdm(keywords, total=len(keywords)):
        for tag in existing_tags:
            if nlp(keyword).has_vector and nlp(tag.lower()).has_vector:
                similarity = nlp(keyword).similarity(nlp(tag.lower()))
                if similarity > threshold:
                    similar_tags.append(tag)

    return list(set(similar_tags))

def process_recipe(index_recipe_existing_tags):
    index, recipe, existing_tags = index_recipe_existing_tags
    combined_text = ' '.join(recipe['ingredients']) + ' ' + ' '.join(recipe['instructions'])

    translator = Translator()
    translated_combined_text = ''
    for i in range(5):  # Retry up to 5 times
        try:
            translated_combined_text = translator.translate(combined_text, dest='en').text
            break  # If the translation is successful, break the loop
        except Exception as e:
            print(f"Translation failed on try {i+1}: {e}")
    similar_tags = find_similar_tags(translated_combined_text, existing_tags, 0.75)
    recipe["tags"] = similar_tags
    return index, recipe

if __name__ == '__main__':
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)

    try:
        with open('progress.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            start_index = data['last_processed_index'] + 1
    except FileNotFoundError:
        start_index = 0

    with open('tags.json', 'r') as f:
        data = json.load(f)
        existing_tags = data["tags"]

    updated_recipes = []
    with multiprocessing.Pool() as pool:
        for index, recipe in pool.imap_unordered(process_recipe, ((index, recipe, existing_tags) for index, recipe in enumerate(recipes[start_index:]))):
            updated_recipes.append((index, recipe))
            updated_recipes.sort()  # Sort by index

            # Extract the recipes just before saving the progress
            recipes_to_save = [recipe for index, recipe in updated_recipes]

            # Save the progress
            # with open('progress_second_half.json', 'w', encoding='utf-8') as f:
            with open('progress1.json', 'w', encoding='utf-8') as f:
                json.dump({'recipes': recipes_to_save, 'last_processed_index': start_index + len(recipes_to_save) - 1}, f, ensure_ascii=False, indent=4)


