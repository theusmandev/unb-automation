import os
from PIL import Image

def convert_to_webp(source_folder, output_folder, quality=80):
    """
    Converts all .png, .jpg, and .jpeg images in a directory to .webp format.
    
    Args:
        source_folder (str): Path to the folder containing source images.
        output_folder (str): Path where converted images will be saved.
        quality (int): Quality of the output WebP image (0-100). Default is 80.
    """
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # valid extensions to look for
    extensions = ('.png', '.jpg', '.jpeg')

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(extensions):
            file_path = os.path.join(source_folder, filename)
            
            try:
                with Image.open(file_path) as img:
                    # Create the new filename with .webp extension
                    file_name_without_ext = os.path.splitext(filename)[0]
                    new_filename = f"{file_name_without_ext}.webp"
                    output_path = os.path.join(output_folder, new_filename)

                    # Save the image
                    # 'optimize=True' helps reduce size further without losing quality
                    img.save(output_path, 'webp', quality=quality, optimize=True)
                    
                    print(f"Converted: {filename} -> {new_filename}")
                    
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")

# --- USAGE ---
# Replace these paths with your actual folder paths
source_dir = r"C:\Users\PCS\Downloads\New folder"
output_dir = r"C:\Users\PCS\Downloads\New folder (2)"

convert_to_webp(source_dir, output_dir, quality=85)