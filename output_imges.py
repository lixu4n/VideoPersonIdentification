import os
import shutil

#mes ficher
source_folder = "subsequence_cam1"
target_folder = "found_images_100_600_obj2"
text_file = "img600_object2_pink.txt"

# Create the target folder if it doesn't exist
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# Read the text file and extract image names
with open(text_file, 'r') as file:
    lines = file.readlines()

# Loop through each line to find and copy images
#this allows us to go through the top similar images histograms frame by frames. .... analyze its accuracy??
for line in lines:
    image_name = line.split(',')[0].split(':')[1].strip() + ".png"
    source_path = os.path.join(source_folder, image_name)
    target_path = os.path.join(target_folder, image_name)
    if os.path.exists(source_path):
        shutil.copyfile(source_path, target_path)
        print(f"Copied {image_name} to {target_folder}")
    else:
        print(f"Image {image_name} not found in {source_folder}")

print("Copying completed.")
