import json
from firebase_admin import credentials, initialize_app, storage
import urllib.parse
from tqdm import tqdm

def normalize_name(name):
    return name.replace("/", "-").replace("\"", "-").replace(":", "-")

cred = credentials.Certificate(r"cred.json")
app = initialize_app(cred, {'storageBucket': 'fridgering.appspot.com'})

bucket_name = "fridgering.appspot.com"

# Get a reference to the storage client
bucket = storage.bucket(app=app)

# List all files in the bucket and convert the iterator to a list
blobs = list(bucket.list_blobs())

# Load the JSON file
with open('ingredients_process.json') as f:
    data = json.load(f)

for item in tqdm(data):
    # Normalize the name
    normalized_name = normalize_name(item['description']+".png")

    for blob in blobs:
        if blob.name == normalized_name:
            # URL encode the file name
            encoded_file_name = urllib.parse.quote(blob.name, safe='')

            # Generate the public URL
            url = f"https://firebasestorage.googleapis.com/v0/b/{bucket_name}/o/{encoded_file_name}?alt=media"
            item['image'] = url

            # print(f"File Name: {blob.name}")
            # print(f"URL: {url}")
            # print("\n")

with open('ingredients_process.json', 'w') as f:
    json.dump(data, f, indent=4)
