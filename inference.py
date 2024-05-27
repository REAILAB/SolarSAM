# Author: Guohao Wang
# this a python script to run the SAM model with the optimal hyperparameters
# it make an obvious segmentation of the image 
# You can change the text prompt to get different results on your image

# the package used in this script is samgeo
# it should be installed before running this script
from samgeo import tms_to_geotiff
from samgeo.text_sam import LangSAM
from PIL import Image
import os
import numpy as np
# import the SAM model
sam = LangSAM()

# text_prompt = 'Roofs of ' + 'Apartment' + ' from satellite'

# path of the image
image_dir = '../../zibo24'
building = {'Apartment','House','Factory','High-rise building','Center building','building'}

# Text prompts for segmentation
text_prompts = {
    'Roofs of ' + 'Apartment' + ' from satellite':0.29,
    'Roofs of ' + 'House' + ' from satellite':0.27,
    'Roofs of ' + 'Center building' + ' from satellite':0.31,
    'Many' + ' Factory ' + 'from satellite':0.29,
    'Overhead shot of the' + 'High-rise building':0.29,
    'Roofs of ' + 'building' + ' from satellite':0.29,
}

# Image resolution and scale
ppi = 196  # pixels per inch
scale_factor = 1110  # scale factor for converting pixel area to real area

# Dictionary to store total pixel count for each text prompt
pixel_counts = {prompt: 0 for prompt in text_prompts}

# Loop through each text prompt
for text_prompt, box_threshold in text_prompts.items():
    # Loop through each image in the directory
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Construct full image path
            image_path = os.path.join(image_dir, filename)

            # Load image
            image = Image.open(image_path)

            # Perform model prediction
            result = sam.predict(image, text_prompt, box_threshold=box_threshold, text_threshold=0.24)

            # Convert result to numpy array for pixel count
            mask = np.array(result['mask'])

            # Count the number of pixels in the mask
            pixel_count = np.sum(mask)

            # Add to the total pixel count for this text prompt
            pixel_counts[text_prompt] += pixel_count

# Calculate the real area for each text prompt
inch_per_pixel = 1 / ppi  # convert pixels to inches
inch_to_meter = 0.0254  # convert inches to meters
area_per_pixel = (inch_per_pixel * inch_to_meter) ** 2  # area of one pixel in square meters

real_areas = []

print("Real area for each text prompt (in square meters):")
for text_prompt, pixel_count in pixel_counts.items():
    real_area = pixel_count * area_per_pixel * scale_factor
    real_areas.append(real_area)
    print(f"{text_prompt}: {real_area:.2f} square meters")
    
i = 1
all_areas = 0
for areas in real_areas:
    if i != 6:
        all_areas = all_areas + areas
        print(areas)
        i = i + 1
    else:
        areas = areas - all_areas
        print(areas)
        print('Finish!')