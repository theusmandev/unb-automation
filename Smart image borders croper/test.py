


# import cv2
# import numpy as np
# import os

# def crop_white_borders(image_path, output_path):
#     # Image read karo
#     img = cv2.imread(image_path)
#     if img is None:
#         print(f"Error reading {image_path}")
#         return
    
#     # Convert to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
#     # Threshold lagao (white area ko detect karne ke liye)
#     _, thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    
#     # Non-white pixels ka bounding box nikaalo
#     coords = cv2.findNonZero(thresh)  
#     x, y, w, h = cv2.boundingRect(coords)
    
#     # Crop karo
#     cropped = img[y:y+h, x:x+w]
    
#     # Save cropped image
#     cv2.imwrite(output_path, cropped)


# def process_folder(input_folder, output_folder):
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
    
#     for filename in os.listdir(input_folder):
#         if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
#             input_path = os.path.join(input_folder, filename)
#             output_path = os.path.join(output_folder, filename)
#             crop_white_borders(input_path, output_path)
#             print(f"Processed: {filename}")


# # Example use
# input_folder = r"C:\Users\PCS\Downloads\nimra ahmed novel pngs\New folder"# yahan apna input folder path do
# output_folder = r"C:\Users\PCS\Downloads\nimra ahmed novel pngs\New folderokok"# yahan output folder path do

# process_folder(input_folder, output_folder)







