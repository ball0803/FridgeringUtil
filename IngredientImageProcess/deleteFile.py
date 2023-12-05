import os

# Read the delete.txt file into a list
with open('delete.txt', 'r') as f:
    delete_files = [line.strip() for line in f]

# Get the directory path
path = "C:\\Users\\COMPUTER\\Desktop\\Ingredient Image"

# Loop through the delete list and remove the files
for file in delete_files:
    file_path = os.path.join(path, file + '.png')  # add .png extension
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"The file {file} does not exist")