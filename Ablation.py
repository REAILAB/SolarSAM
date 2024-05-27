# Author: Guohao Wang
# This is a python script to run the SAM model with a text prompt
# for the ablation study of the SAM model with different text prompts and box thresholds

# The package used in this script is samgeo
# It should be installed before running this script
# from samgeo import tms_to_geotiff
from samgeo.text_sam import LangSAM
import numpy as np
import cv2  # OpenCV for loading images
import pandas as pd  # Import pandas for saving results to Excel

# Import the SAM model
sam = LangSAM()

building = ['Apartment', 'House', 'Factory', 'High-rise building', 'Center building', 'building']

# Path of the image and labels
Path = '../../subset/'
PathLabel = '../../subset_label/'

# Function to load ground truth mask
def load_ground_truth_mask(label_path):
    mask = cv2.imread(label_path, cv2.IMREAD_GRAYSCALE)
    return mask / 255  # Normalize to binary mask (0 or 1)

# Dataframes to store results
iou_results = []
pa_results = []

# Loop through each building type and text prompt combination for IoU
for buildingtype in building:
    for i in range(1, 7):
        if i == 1:
            text_prompt = buildingtype
        elif i == 2:
            text_prompt = buildingtype + ' from satellite'
        elif i == 3:
            text_prompt = 'Roofs of ' + buildingtype
        elif i == 4:
            text_prompt = 'Roofs of ' + buildingtype + ' from satellite'
        elif i == 5:
            text_prompt = 'Overhead shot of the ' + buildingtype
        elif i == 6:
            text_prompt = 'Many ' + buildingtype + ' from satellite'
        
        iou_scores = []
        for figure in range(1, 101):
            image_path = Path + str(figure) + '.jpg'
            label_path = PathLabel + str(figure) + '.png'
            
            # Model prediction
            sam.predict(image_path, text_prompt, box_threshold=0.29, text_threshold=0.24)
            predicted_mask = sam.shown_anns()

            # Load ground truth label
            ground_truth_mask = load_ground_truth_mask(label_path)

            # Calculate mIoU
            intersection = np.logical_and(predicted_mask, ground_truth_mask)
            union = np.logical_or(predicted_mask, ground_truth_mask)
            iou_score = np.sum(intersection) / np.sum(union)
            iou_scores.append(iou_score)

        # Calculate average IoU for this text prompt
        avg_iou = np.mean(iou_scores)
        iou_results.append([buildingtype, text_prompt, avg_iou])

# Convert IoU results to DataFrame and save to Excel
iou_df = pd.DataFrame(iou_results, columns=['BuildingType', 'TextPrompt', 'AverageIoU'])
iou_df_pivot = iou_df.pivot(index='BuildingType', columns='TextPrompt', values='AverageIoU')
iou_df_pivot.to_excel('iou_results.xlsx')

# Loop through each building type and box threshold for PA
for buildingtype in building:
    for i in range(11, 40):
        box_threshold = i / 100
        pa_scores = []
        for figure in range(1, 101):
            image_path = Path + str(figure) + '.jpg'
            label_path = PathLabel + str(figure) + '.png'
            
            # Model prediction
            sam.predict(image_path, text_prompt, box_threshold=box_threshold, text_threshold=0.24)
            predicted_mask = sam.shown_anns()

            # Load ground truth label
            ground_truth_mask = load_ground_truth_mask(label_path)

            # Calculate PA
            correct = np.sum(predicted_mask == ground_truth_mask)
            total = ground_truth_mask.size
            accuracy = correct / total
            pa_scores.append(accuracy)

        # Calculate average PA for this box threshold
        avg_pa = np.mean(pa_scores)
        pa_results.append([buildingtype, box_threshold, avg_pa])

# Convert PA results to DataFrame and save to Excel
pa_df = pd.DataFrame(pa_results, columns=['BuildingType', 'BoxThreshold', 'AveragePA'])
pa_df_pivot = pa_df.pivot(index='BuildingType', columns='BoxThreshold', values='AveragePA')
pa_df_pivot.to_excel('pa_results.xlsx')