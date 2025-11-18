

import cv2
import numpy as np
import os

def crop_white_borders(image_path, output_path, threshold=250):
    try:
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not read {image_path}")
            return False

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold to detect white areas
        _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
        
        # Find non-white pixels
        coords = cv2.findNonZero(thresh)
        if coords is None:
            print(f"Error: No non-white content found in {image_path}")
            return False
        
        # Get bounding box
        x, y, w, h = cv2.boundingRect(coords)
        
        # Ensure bounding box is valid
        if w == 0 or h == 0:
            print(f"Error: Invalid bounding box for {image_path}")
            return False
        
        # Crop image
        cropped = img[y:y+h, x:x+w]
        
        # Save cropped image
        cv2.imwrite(output_path, cropped)
        return True
    
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return False

def process_folder(input_folder, output_folder, threshold=250):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Process each image file
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            # Avoid overwriting by adding a suffix if file exists
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(output_path):
                output_path = os.path.join(output_folder, f"{base}_{counter}{ext}")
                counter += 1
            
            # Process the image
            if crop_white_borders(input_path, output_path, threshold):
                print(f"Processed: {filename} -> {os.path.basename(output_path)}")
            else:
                print(f"Failed to process: {filename}")

# Example usage
input_folder = r"C:\Users\PCS\Downloads\New folder"
output_folder = r"C:\Users\PCS\Downloads\New folderokok"

process_folder(input_folder, output_folder, threshold=240)  # Lowered threshold for flexibility



