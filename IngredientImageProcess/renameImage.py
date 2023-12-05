import os

# Read the text file into a list
with open('descriptions.txt', 'r') as f:
    new_names = [line.strip() for line in f]  # remove .png here
    new_names = [name.replace('/', '-').replace('"', '-').replace(':', '-')[:200] + '.png' for name in new_names]  # append .png here

# Get a list of current image files
path1 = "C:\\Users\\COMPUTER\\Desktop\\2023-11-25"
path2 = "C:\\Users\\COMPUTER\\Desktop\\2023-11-26"
previous_files = os.listdir(path1)  # replace with your directory
current_files = os.listdir(path2)  # replace with your directory

# Rename the files
for old_name, new_name in zip(sorted(current_files), new_names[len(previous_files):]):
    os.rename(os.path.join(path2, old_name), os.path.join(path2, new_name))